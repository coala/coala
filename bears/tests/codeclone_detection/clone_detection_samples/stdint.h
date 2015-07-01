/* stdint.h
 *
 * This file tries to follow the standardizations specified in the POSIX
 * Programmers Manual wich can be reached through
 * 		http://pubs.opengroup.org/onlinepubs/009695399/basedefs/stdint.h.html
 *
 * See also:
 * 		http://sourceforge.net/p/predef/wiki/DataModels/
 *
 * Copyright (C) 2013 Lasse Schuirmann. All Rights Reserved.
 * Written by Lasse Schuirmann (lasse.schuirmann@gmail.com)
 *
 * This program is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later
 * version.
 */

#ifndef _STDINT_H
#define _STDINT_H

#include <settings.h>

//in addition to posix
typedef unsigned char		bool;

typedef signed char			int8_t;
typedef unsigned char		uint8_t;
typedef short				int16_t;
typedef unsigned short		uint16_t;
typedef long				int32_t;
typedef unsigned long		uint32_t;
#ifdef __x86_64__
#warning "Assumed LP64 mode!"
typedef long long			int64_t;
typedef unsigned long long	uint64_t;
#endif

#ifdef __i386__
typedef uint32_t			uintptr_t;
typedef int32_t				intptr_t;
#elif defined __x86_64__
typedef uint64_t			uintptr_t;
typedef int64_t				intptr_t;
#endif

// TODO least, fast, greatest

#endif /* _STDINT_H */
