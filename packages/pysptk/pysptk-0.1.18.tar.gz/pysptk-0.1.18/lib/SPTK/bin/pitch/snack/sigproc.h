#ifndef SIGPROC_H_
#define SIGPROC_H_

#define BIGSORD 100

#define Fprintf (void) fprintf

int xget_window(register float *dout, register int n, register int type);
void xrwindow(register float *din, register float *dout, register int n,
              register float preemp);
void xcwindow(register float *din, register float *dout, register int n,
              register float preemp);
void xhwindow(register float *din, register float *dout, register int n,
              register float preemp);
void xhnwindow(register float *din, register float *dout, register int n,
               register float preemp);
int sigproc_window(register float *din, register float *dout, register int n,
                   register float preemp, int type);
void xautoc(register int windowsize, register float *s, register int p,
            register float *r, register float *e);
void xdurbin(register float *r, register float *k, register float *a,
             register int p, register float *ex);
void xa_to_aca(float *a, float *b, float *c, register int p);
float xitakura(register int p, register float *b, register float *c,
               register float *r, register float *gain);
float wind_energy(register float *data, register int size, register int w_type);
int xlpc(int lpc_ord, float lpc_stabl, int wsize, float *data, float *lpca,
         float *ar, float *lpck, float *normerr, float *rms, float preemp,
         int type);
void crossf(float *data, int size, int start, int nlags, float *engref,
            int *maxloc, float *maxval, float *correl);
void crossfi(float *data, int size, int start0, int nlags0, int nlags,
             float *engref, int *maxloc, float *maxval, float *correl,
             int *locs, int nlocs);

#endif /* SIGPROC_H_ */
