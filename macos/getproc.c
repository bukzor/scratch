#include <stdio.h>  /* printf */
#include <sys/_types/_caddr_t.h>
#include <unistd.h>  /* getpid */
#include <stdlib.h>  /* atoi */
#include <sys/sysctl.h>  /* sysctl CTL_KERN KERN_PROC_ALL kinfo_proc */
#include <sys/proc.h> /* extern_proc */

struct kinfo_proc* pgetproc(int pid) {
    int mib[] = { CTL_KERN, KERN_PROC, KERN_PROC_PID, pid};
    size_t len;
    int ret = sysctl(mib, 4, NULL, &len, NULL, 0);
    if (ret < 0) {
      perror("while retrieving sysctl result size");
      return NULL;
    }

    struct kinfo_proc* result = malloc(len);
    // sysctl(int *name, u_int namelen, void *oldp, size_t *oldlenp, void *newp, size_t newlen);
    ret = sysctl(mib, 4, result, &len, NULL, 0);
    if (ret < 0) {
      perror("during sysctl");
      return NULL;
    }
    return result;
}


// , caddr_t: showf(p, x)
#define showf(format, name) printf(#name ": %" #format "\n", name)

#define show_str(name) showf(  s, name)

#define show_chr(name)    showf(hhi, name)
#define show_short(name)  showf( hi, name)
#define show_int(name)    showf(  i, name)
#define show_long(name)   showf( li, name)
#define show_lll(name)    showf(lli, name)

#define show_uchr(name)   showf(hhu, name)
#define show_ushort(name) showf( hu, name)
#define show_uint(name)   showf(  u, name)
#define show_ulong(name)  showf( lu, name)
#define show_ull(name)    showf(llu, name)

#define _nullcheck(name, ifnotnull) \
  if ( name == NULL ) { \
    printf(#name ": NULL\n"); \
  } else { \
    ifnotnull; \
  };

#define show_ptr(name) \
  _nullcheck(name, print_blob(#name, sizeof(void *), &(name)))

#define show_pid(name)    show_uint(name)
#define show_undef(name)  show_ptr(name)  // would be: show_blobp

#define show_blob(name) \
  print_blob(#name, sizeof(name), &(name))
#define show_blobp(name, ifnotnull) \
  _nullcheck(name, ifnotnull)


void print_blob(char* label, unsigned int blobsize, void* blob) {
  char* bytes = (char*)blob;
  printf("%s: 0x", label);
  for (int  i = blobsize - 1; i >= 0; i--) {
    printf("%02hhx", bytes[i]);
    if (i > 0 && i % 4 == 0) {
      printf(" ");
    }
  }
  printf("\n");
}


int main(int argc, char** argv) {
  int pid;
  if ( argc == 1 ) {
    pid = getpid();
  } else if ( argc == 2 ) {
    pid = atoi(argv[1]);
  } else {
    return 1;
  }

  struct kinfo_proc *proc;
  proc = pgetproc(pid);
  if (proc == NULL) {
    return -1;
  }

  // pid_t: int
  // caddr_t: char*
  // void *: hex
  // boolean_t: int
  // u_int: unsigned int
  // fixpt_t: unsigned int
  // u_quad_t: unsigned long long
  // sigset_t: hex
  // u_char: unsigned char
  // dev_t: int
  // segsz_t: int
  // struct timeval { long tv_sec; int tv_usec; }

  // "incomplete type"
  show_undef (proc->kp_proc.p_un.p_st1.__p_forw);        // struct proc *
  // "incomplete type"
  show_undef (proc->kp_proc.p_un.p_st1.__p_back);        // struct proc *
  show_long  (proc->kp_proc.p_un.__p_starttime.tv_sec);  // long
  show_int   (proc->kp_proc.p_un.__p_starttime.tv_usec); // int
  if (proc->kp_proc.p_vmspace == NULL) {                 // struct vmspace*   address space
    show_ptr   (proc->kp_proc.p_vmspace);
  } else {
    show_int   (proc->kp_proc.p_vmspace->dummy);         // int32_t   just to keep kinfo_proc happy */
    show_ptr   (proc->kp_proc.p_vmspace->dummy2);        // caddr_t
    show_blob  (proc->kp_proc.p_vmspace->dummy3);        // int32_t
    show_blob  (proc->kp_proc.p_vmspace->dummy4);        // caddr_t
  }
  // "incomplete type"
  show_undef (proc->kp_proc.p_sigacts);                  // struct sigacts*
  show_int   (proc->kp_proc.p_flag);                     // int
  show_int   (proc->kp_proc.p_stat);                     // char
  show_pid   (proc->kp_proc.p_pid);                      // pid_t
  show_pid   (proc->kp_proc.p_oppid);                    // pid_t
  show_int   (proc->kp_proc.p_dupfd);                    // int
  show_ptr   (proc->kp_proc.user_stack);                 // caddr_t
  show_ptr   (proc->kp_proc.exit_thread);                // void *
  show_int   (proc->kp_proc.p_debugger);                 // int
  show_int   (proc->kp_proc.sigwait);                    // boolean_t
  show_uint  (proc->kp_proc.p_estcpu);                   // u_int
  show_int   (proc->kp_proc.p_cpticks);                  // int
  show_uint  (proc->kp_proc.p_pctcpu);                   // fixpt_t
  show_ptr   (proc->kp_proc.p_wchan);                    // void *    Sleep address.
  show_str   (proc->kp_proc.p_wmesg);                    // char *    Reason for sleep.
  show_uint  (proc->kp_proc.p_swtime);                   // u_int     Time swapped in or out.
  show_uint  (proc->kp_proc.p_slptime);                  // u_int     Time since last blocked.
  show_long  (proc->kp_proc.p_realtimer.it_interval.tv_sec);   // long      Alarm timer interval
  show_int   (proc->kp_proc.p_realtimer.it_interval.tv_usec);  // int       Alarm timer interval
  show_long  (proc->kp_proc.p_realtimer.it_value.tv_sec);      // long      Alarm timer current value
  show_int   (proc->kp_proc.p_realtimer.it_value.tv_usec);     // int       Alarm timer current value
  show_long  (proc->kp_proc.p_rtime.tv_sec);             // long      Real time.
  show_int   (proc->kp_proc.p_rtime.tv_usec);            // int       Real time.
  show_ull   (proc->kp_proc.p_uticks);                   // u_quad_t  Statclock hits in user mode.
  show_ull   (proc->kp_proc.p_sticks);                   // u_quad_t  Statclock hits in system mode.
  show_ull   (proc->kp_proc.p_iticks);                   // u_quad_t  Statclock hits processing intr.
  show_int   (proc->kp_proc.p_traceflag);                // int       Kernel trace points.
  // "incomplete type"
  show_undef (proc->kp_proc.p_tracep);                   // struct vnode *    Trace to vnode.
  show_int   (proc->kp_proc.p_siglist);                  // int       DEPRECATED.
  // "incomplete type"
  show_undef (proc->kp_proc.p_textvp);                   // struct vnode *    Vnode of executable.
  show_int   (proc->kp_proc.p_holdcnt);                  // int       If non-zero, don't swap.
  show_blob  (proc->kp_proc.p_sigmask);                  // sigset_t  DEPRECATED.
  show_blob  (proc->kp_proc.p_sigignore);                // sigset_t  Signals being ignored.
  show_blob  (proc->kp_proc.p_sigcatch);                 // sigset_t  Signals being caught by user.
  show_uchr  (proc->kp_proc.p_priority);                 // u_char    Process priority.
  show_uchr  (proc->kp_proc.p_usrpri);                   // u_char    User-priority based on p_cpu and p_nice.
  show_chr   (proc->kp_proc.p_nice);                     // char      Process "nice" value.
  show_str   (proc->kp_proc.p_comm);                     // char *
  // "incomplete type"
  show_undef (proc->kp_proc.p_pgrp);                     // struct pgrp *     Pointer to process group.
  // "incomplete type"
  show_undef (proc->kp_proc.p_addr);                     // struct user *     Kernel virtual addr of u-area (PROC ONLY).
  show_ushort (proc->kp_proc.p_xstat);                   // u_short   Exit status for wait; also stop signal.
  show_ushort (proc->kp_proc.p_acflag);                  // u_short   Accounting flags.
  if (proc->kp_proc.p_ru == NULL) {
    show_ptr(proc->kp_proc.p_ru);                        // struct rusage *  Exit information.
  } else {
    show_long  (proc->kp_proc.p_ru->ru_utime.tv_sec);    // long      user time used (PL)
    show_int   (proc->kp_proc.p_ru->ru_utime.tv_usec);   // int       user time used (PL)
    show_long  (proc->kp_proc.p_ru->ru_stime.tv_sec);    // long      system time used (PL)
    show_int   (proc->kp_proc.p_ru->ru_stime.tv_usec);   // int       system time used (PL)
    show_long  (proc->kp_proc.p_ru->ru_maxrss);          // long      max resident set size (PL)
    show_long  (proc->kp_proc.p_ru->ru_ixrss);           // long      integral shared memory size (NU)
    show_long  (proc->kp_proc.p_ru->ru_idrss);           // long      integral unshared data (NU)
    show_long  (proc->kp_proc.p_ru->ru_isrss);           // long      integral unshared stack (NU)
    show_long  (proc->kp_proc.p_ru->ru_minflt);          // long      page reclaims (NU)
    show_long  (proc->kp_proc.p_ru->ru_majflt);          // long      page faults (NU)
    show_long  (proc->kp_proc.p_ru->ru_nswap);           // long      swaps (NU)
    show_long  (proc->kp_proc.p_ru->ru_inblock);         // long      block input operations (atomic)
    show_long  (proc->kp_proc.p_ru->ru_oublock);         // long      block output operations (atomic)
    show_long  (proc->kp_proc.p_ru->ru_msgsnd);          // long      messages sent (atomic)
    show_long  (proc->kp_proc.p_ru->ru_msgrcv);          // long      messages received (atomic)
    show_long  (proc->kp_proc.p_ru->ru_nsignals);        // long      signals received (atomic)
    show_long  (proc->kp_proc.p_ru->ru_nvcsw);           // long      voluntary context switches (atomic)
    show_long  (proc->kp_proc.p_ru->ru_nivcsw);          // long      involuntary "
  }
  // "incomplete type"
  show_undef (proc->kp_eproc.e_paddr);                   // struct proc *     address of proc
  // "incomplete type"
  show_undef (proc->kp_eproc.e_sess);                    // struct session *  session pointer
  // >>>      proc->kp_eproc.e_pcred                     // struct _pcred     process credentials
  show_blob  (proc->kp_eproc.e_pcred.pc_lock);           /* char      opaque content */
  // "incomplete type"
  show_undef (proc->kp_eproc.e_pcred.pc_ucred);          /* struct ucred * Current credentials. */
  show_int   (proc->kp_eproc.e_pcred.p_ruid);            /* uid_t     Real user id. */
  show_int   (proc->kp_eproc.e_pcred.p_svuid);           /* uid_t     Saved effective user id. */
  show_int   (proc->kp_eproc.e_pcred.p_rgid);            /* gid_t     Real group id. */
  show_int   (proc->kp_eproc.e_pcred.p_svgid);           /* gid_t     Saved effective group id. */
  show_int   (proc->kp_eproc.e_pcred.p_refcnt);          /* int       Number of references. */
  // todo: expand
  //         (proc->kp_eproc.e_ucred)                    // struct _ucred     current credentials
  show_int   (proc->kp_eproc.e_ucred.cr_ref);            /* int32_t   reference count */
  show_int   (proc->kp_eproc.e_ucred.cr_uid);            /* uid_t     effective user id */
  show_int   (proc->kp_eproc.e_ucred.cr_ngroups);        /* short     number of groups */
  show_blob  (proc->kp_eproc.e_ucred.cr_groups);         /* gid_t[NGROUPS]    groups */
  show_blob  (proc->kp_eproc.e_vm);                      // struct vmspace    address space
  show_pid   (proc->kp_eproc.e_ppid);                    // pid_t     parent process id
  show_pid   (proc->kp_eproc.e_pgid);                    // pid_t     process group id
  show_short (proc->kp_eproc.e_jobc);                    // short     job control counter
  show_int   (proc->kp_eproc.e_tdev);                    // dev_t     controlling tty dev
  show_pid   (proc->kp_eproc.e_tpgid);                   // pid_t     tty process group id
  // "incomplete type"
  show_undef (proc->kp_eproc.e_tsess);                   // struct session *  tty session pointer
  show_str   (proc->kp_eproc.e_wmesg);                   // char*     wchan message
  show_int   (proc->kp_eproc.e_xsize);                   // segsz_t   text size
  show_short (proc->kp_eproc.e_xrssize);                 // short     text rss
  show_short (proc->kp_eproc.e_xccount);                 // short     text references
  show_short (proc->kp_eproc.e_xswrss);                  // short
  show_int   (proc->kp_eproc.e_flag);                    // int32_t
  show_str   (proc->kp_eproc.e_login);                   // char*     short setlogin() name
  show_blob  (proc->kp_eproc.e_spare);                   // int32_t


  printf("pid: %d, process groupd id: %d, session ID: %d\n", pid, getpgid(pid), getsid(pid));
}
