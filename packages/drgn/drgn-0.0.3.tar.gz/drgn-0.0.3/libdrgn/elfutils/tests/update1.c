/* Test program for elf_update function.
   Copyright (C) 2000, 2002, 2005 Red Hat, Inc.
   This file is part of elfutils.
   Written by Ulrich Drepper <drepper@redhat.com>, 2000.

   This file is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   elfutils is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#ifdef HAVE_CONFIG_H
# include <config.h>
#endif

#include <errno.h>
#include <fcntl.h>
#include <libelf.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


int
main (int argc, char *argv[] __attribute__ ((unused)))
{
  const char *fname = "xxx_update1";
  int fd;
  Elf *elf;
  Elf32_Ehdr *ehdr;
  int i;

  fd = open (fname, O_RDWR | O_CREAT | O_TRUNC, 0666);
  if (fd == -1)
    {
      printf ("cannot open `%s': %s\n", fname, strerror (errno));
      exit (1);
    }

  elf_version (EV_CURRENT);

  elf = elf_begin (fd, ELF_C_WRITE, NULL);
  if (elf == NULL)
    {
      printf ("cannot create ELF descriptor: %s\n", elf_errmsg (-1));
      exit (1);
    }

  /* Create an ELF header.  */
  ehdr = elf32_newehdr (elf);
  if (ehdr == NULL)
    {
      printf ("cannot create ELF header: %s\n", elf_errmsg (-1));
      exit (1);
    }

  /* Print the ELF header values.  */
  if (argc > 1)
    {
      for (i = 0; i < EI_NIDENT; ++i)
	printf (" %02x", ehdr->e_ident[i]);
      printf ("\
\ntype = %hu\nmachine = %hu\nversion = %u\nentry = %u\nphoff = %u\n"
	      "shoff = %u\nflags = %u\nehsize = %hu\nphentsize = %hu\n"
	      "phnum = %hu\nshentsize = %hu\nshnum = %hu\nshstrndx = %hu\n",
	      ehdr->e_type, ehdr->e_machine, ehdr->e_version, ehdr->e_entry,
	      ehdr->e_phoff, ehdr->e_shoff, ehdr->e_flags, ehdr->e_ehsize,
	      ehdr->e_phentsize, ehdr->e_phnum, ehdr->e_shentsize,
	      ehdr->e_shnum, ehdr->e_shstrndx);
    }

  ehdr->e_ident[0] = 42;
  ehdr->e_ident[4] = 1;
  ehdr->e_ident[5] = 1;
  ehdr->e_ident[6] = 2;
  ehdr->e_ident[9] = 2;
  ehdr->e_version = 1;
  ehdr->e_ehsize = 1;

  /* Write out the file.  */
  if (elf_update (elf, ELF_C_WRITE) < 0)
    {
      printf ("failure in elf_update: %s\n", elf_errmsg (-1));
      exit (1);
    }

  /* Create an ELF header.  */
  ehdr = elf32_newehdr (elf);
  if (ehdr == NULL)
    {
      printf ("cannot create ELF header: %s\n", elf_errmsg (-1));
      exit (1);
    }

  /* Print the ELF header values.  */
  if (argc > 1)
    {
      for (i = 0; i < EI_NIDENT; ++i)
	printf (" %02x", ehdr->e_ident[i]);
      printf ("\
\ntype = %hu\nmachine = %hu\nversion = %u\nentry = %u\nphoff = %u\n"
	      "shoff = %u\nflags = %u\nehsize = %hu\nphentsize = %hu\n"
	      "phnum = %hu\nshentsize = %hu\nshnum = %hu\nshstrndx = %hu\n",
	      ehdr->e_type, ehdr->e_machine, ehdr->e_version, ehdr->e_entry,
	      ehdr->e_phoff, ehdr->e_shoff, ehdr->e_flags, ehdr->e_ehsize,
	      ehdr->e_phentsize, ehdr->e_phnum, ehdr->e_shentsize,
	      ehdr->e_shnum, ehdr->e_shstrndx);
    }

  if (elf_end (elf) != 0)
    {
      printf ("failure in elf_end: %s\n", elf_errmsg (-1));
      exit (1);
    }

  unlink (fname);

  return 0;
}
