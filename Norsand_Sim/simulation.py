# simulation.py
import numpy as np
from material import compute_gmax, compute_ec, compute_yield_function

class NorSandTriaxialSimulation:
    def __init__(self, params):
        self.n = params["N"]
        self.lambda_ = params["lambda"]
        self.mc = params["Mc"]
        self.chi = params["chi"]
        self.k0 = params["K0"]
        self.e0 = params["e0"]
        self.sigm0 = params["sigM0"]
        self.pref = 100.0
        self.k_over_g = params.get("K_over_G", 2.0)
        self.h0 = params.get("H0", 5.0)
        self.hy = params.get("HY", 10.0)

        self.num_steps = params.get("num_steps", 4000)
        self.max_strain = params.get("max_strain", 0.3)
        self.undrained = params.get("undrained", False)

        self.e = self.e0
        self.sigm = self.sigm0
        self.sigq = 0.0
        self.pimg = self.sigm0
        self.ep1 = 0.0
        self.epv = 0.0
        self.u = 0.0

        self.results = []

    def run(self):
        d_eps = self.max_strain / (self.num_steps - 1)

        for step in range(self.num_steps):
            gmax = compute_gmax(self.e, self.sigm)
            kmax = gmax * self.k_over_g
            ec = compute_ec(self.n, self.lambda_, self.sigm, self.pref)
            psi = self.e - ec
            f = compute_yield_function(self.sigq, self.sigm, psi, self.pimg, self.mc, self.n)

            if f <= 0:
                # Elastic predictor
                dep1 = d_eps
                depv = 0.0 if self.undrained else dep1 / 3
                self.sigq += 3 * gmax * (dep1 - depv / 3)
                self.sigm += 0 if self.undrained else kmax * depv
                self.u += 0 if not self.undrained else kmax * dep1 / 3
            else:
                # Plastic corrector
                depg = d_eps
                d = self.chi * psi
                depv = d * depg
                dep1 = depg + depv / 3

                dsigq = 3 * gmax * (dep1 - depv / 3)
                dsigm = kmax * depv

                self.sigq += dsigq
                if self.undrained:
                    self.u += dsigm
                else:
                    self.sigm += dsigm
                    self.e -= (1 + self.e) * depv

                h = self.h0 + self.hy * psi
                self.pimg += h * depg * self.pimg

            self.ep1 += d_eps
            self.epv += depv

            self.results.append({
                "step": step,
                "eps1": self.ep1,
                "epsV": self.epv,
                "p": self.sigm - self.u if self.undrained else self.sigm,
                "q": self.sigq,
                "e": self.e,
                "psi": psi,
                "pimg": self.pimg,
                "yield_f": f,
                "pore_pressure": self.u if self.undrained else 0.0,
            })

        return self.results
