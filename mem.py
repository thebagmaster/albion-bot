import ctypes
import win32process
import win32con
from ctypes import *
from ctypes.wintypes import *
import win32ui
import numpy as np
from struct import *
import sys

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
WriteProcessMemory = windll.kernel32.WriteProcessMemory
CloseHandle = windll.kernel32.CloseHandle
CreateToolhelp32Snapshot= windll.kernel32.CreateToolhelp32Snapshot
Module32First = windll.kernel32.Module32First
Module32Next = windll.kernel32.Module32Next
Thread32Next = windll.kernel32.Thread32Next


SYNCHRONIZE = 0x00100000;
STANDARD_RIGHTS_REQUIRED = 0x000F0000;
PROCESS_ALL_ACCESS        = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF);

HWND = win32ui.FindWindow(None,u'Albion Online Client').GetSafeHwnd()
TID,PID = win32process.GetWindowThreadProcessId(HWND)
processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, PID)
#print(processHandle)
buffer = c_char_p(b"The data goes here")
bufferSize = len(buffer.value)

class MODULEENTRY32(Structure):
    _fields_ = [( 'dwSize' , DWORD ) ,
                ( 'th32ModuleID' , DWORD ),
                ( 'th32ProcessID' , DWORD ),
                ( 'GlblcntUsage' , DWORD ),
                ( 'ProccntUsage' , DWORD ) ,
                ( 'modBaseAddr' , POINTER(BYTE) ) ,
                ( 'modBaseSize' , DWORD ) ,
                ( 'hModule' , HMODULE ) ,
                ( 'szModule' , c_char * 256 ),
                ( 'szExePath' , c_char * 260 ) ]

def GetBaseAddress(pid):
    TH32CS_SNAPMODULE = 0x00000008
    hModuleSnap = DWORD
    me32 = MODULEENTRY32()
    me32.dwSize = sizeof( MODULEENTRY32 )
    #me32.dwSize = 5000
    hModuleSnap = CreateToolhelp32Snapshot( TH32CS_SNAPMODULE, pid )
    ret = Module32First( hModuleSnap, pointer(me32) )
    if ret == 0 :
        print('ListProcessModules() Error on Module32First[%d]' % GetLastError())
        CloseHandle( hModuleSnap )
    return ctypes.addressof(me32.modBaseAddr.contents) # Get the base address of first module since this is the RocketLeague.exe one

BASE = GetBaseAddress(PID)

def search(base,match_val):
    match_val = np.asarray(list(pack('<L',match_val)))
    #print(match_val)
    chunk_start_adr = base
    indices = []
    a_s= []

    while chunk_start_adr <= base+0x10000 or chunk_start_adr < 0xF0000000:
        bytesRead = c_ulong(0)
        a = np.zeros(0x100000, 'B')     # chunk size; should be even bigger ..
        #print (a.itemsize)
        r = ReadProcessMemory(processHandle, c_ulonglong(chunk_start_adr), a.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)), a.itemsize * a.size, byref(bytesRead))
        #print (hex(chunk_start_adr),match_val,a)
        if r:
            new, = np.where(a == match_val[0])   # fast bulk search
            #new, = np.nonzero(np.in1d(a,match_val))
            if len(new) > 0:
                for n in new:
                    try:
                        if((a[n:n+4]==match_val).all()):
                            indices.append((chunk_start_adr+n))
                            #print(hex(chunk_start_adr+n),len(indices))
                        #print (hex(chunk_start_adr),new,a[n-3:n+3],hex(chunk_start_adr + n))
                    except:
                        pass
        chunk_start_adr += a.itemsize * a.size
    return indices

def readMem64(address, offset):
    val = c_ulonglong()
    bytesRead = c_ulong(0)
    for i in range(len(offset)):

        if ReadProcessMemory(processHandle, c_ulonglong(address+offset[i]), buffer, bufferSize, byref(bytesRead)):
            memmove(ctypes.byref(val), buffer, ctypes.sizeof(val))
            address = val.value
        else:
            return -1

    return c_ulonglong(val.value).value

def readMem(address, offset):
    val = c_ulong()
    bytesRead = c_ulonglong(0)

    for i in range(len(offset)):
        #print (hex(address))
        if ReadProcessMemory(processHandle, c_ulonglong(address+offset[i]), buffer, bufferSize, byref(bytesRead)):
            memmove(ctypes.byref(val), buffer, ctypes.sizeof(val))
            address = val.value
        else:
            #print windll.kernel32.GetLastError()
            return -1

    return c_ulong(val.value).value

def readMemFloat(address, offset):
    val = c_ulong()
    bytesRead = c_ulong(0)

    for i in range(len(offset)):
        #print (hex(address),address+offset[i],hex(address+offset[i]))
        if ReadProcessMemory(processHandle, c_ulonglong(address+offset[i]), buffer, bufferSize, byref(bytesRead)):
            memmove(ctypes.byref(val), buffer, ctypes.sizeof(val))
            address = val.value
        else:
            return float("inf")
    val = c_float()
    memmove(ctypes.byref(val), buffer, ctypes.sizeof(val))
    #print(val.value)
    return val.value
    # if ReadProcessMemory(processHandle, address, buffer, bufferSize, byref(bytesRead)):
        # memmove(ctypes.byref(val), buffer, ctypes.sizeof(val))
        # if ReadProcessMemory(processHandle, val.value + offset, buffer, bufferSize, byref(bytesRead)):
            # memmove(ctypes.byref(val), buffer, ctypes.sizeof(val))
            # return val.value
        # else:
            # return -1

        # return val.value
    # else:
        # return -1

def writeMem(address, val):
    count = c_ulong(0)

    c_data = c_float(val)
    length = ctypes.sizeof(c_data)
    memmove(buffer, ctypes.byref(c_data), ctypes.sizeof(c_data))
    if not windll.kernel32.WriteProcessMemory(processHandle, c_ulonglong(address), buffer, length, byref(count)):
        print  ("Failed: Write Memory - Error Code: ", windll.kernel32.GetLastError() , str(val))
        windll.kernel32.SetLastError(10000)
    else:
        return False
