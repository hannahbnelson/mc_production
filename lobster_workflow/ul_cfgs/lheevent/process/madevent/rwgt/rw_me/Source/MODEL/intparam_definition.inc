ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      written by the UFO converter
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

C     Parameters that should not be recomputed event by event.
C     
      IF(READLHA) THEN

        G = 2 * DSQRT(AS*PI)  ! for the first init

        MDL_CW0 = MDL_MW/MDL_MZ

        MDL_SQRT__2 = SQRT(DCMPLX(2.000000D+00))

        MDL_MUH0 = MDL_MH/MDL_SQRT__2

        MDL_MW__EXP__2 = MDL_MW**2

        MDL_MZ__EXP__2 = MDL_MZ**2

        MDL_SW0 = SQRT(DCMPLX(1.000000D+00-MDL_MW__EXP__2
     $   /MDL_MZ__EXP__2))

        MDL_CF3PL1 = MDL_C3PL1

        MDL_CF3PL2 = MDL_C3PL2

        MDL_CFLL = 2.000000D+00*MDL_CLL1221

        MDL_NB__2__EXP__0_25 = 2.000000D+00**2.500000D-01

        MDL_LAMBDA__EXP__2 = MDL_LAMBDA**2

        MDL_CTB = (-MDL_CTZ+MDL_CTW*MDL_CW0)/MDL_SW0

        MDL_CW0__EXP__2 = MDL_CW0**2

        MDL_SW0__EXP__2 = MDL_SW0**2

        MDL_MH__EXP__2 = MDL_MH**2

        MDL_COMPLEXI = DCMPLX(0.000000D+00,1.000000D+00)

        MDL_SW0__EXP__3 = MDL_SW0**3

        MDL_CW0__EXP__3 = MDL_CW0**3

        MDL_MT__EXP__2 = MDL_MT**2

        MDL_MT__EXP__3 = MDL_MT**3

        MDL_MUEFT__EXP__2 = MDL_MUEFT**2

        MDL_VEV0 = SQRT(DCMPLX(1.000000D+00/MDL_GF))
     $   /MDL_NB__2__EXP__0_25

        MDL_VEV0__EXP__2 = MDL_VEV0**2

        MDL_DT = (MDL_CPDC*MDL_VEV0__EXP__2)/(2.000000D+00
     $   *MDL_LAMBDA__EXP__2)

        MDL_DV = ((MDL_CF3PL1+MDL_CF3PL2-MDL_CFLL/2.000000D+00)
     $   *MDL_VEV0__EXP__2)/MDL_LAMBDA__EXP__2

        MDL_DWB = (MDL_CPWB*MDL_VEV0__EXP__2)/MDL_LAMBDA__EXP__2

        MDL_DLAM = ((4.000000D+00*MDL_CDP-MDL_CPDC)*MDL_VEV0__EXP__2)
     $   /(2.000000D+00*MDL_LAMBDA__EXP__2)

        MDL_EE0 = (2.000000D+00*MDL_MW*MDL_SW0)/MDL_VEV0

        MDL_CW = MDL_CW0*(1.000000D+00+MDL_DT/2.000000D+00)

        MDL_MUH = (1.000000D+00-MDL_DLAM/2.000000D+00)*MDL_MUH0

        MDL_SW = (1.000000D+00-(MDL_CW0__EXP__2*MDL_DT)/(2.000000D+00
     $   *MDL_SW0__EXP__2))*MDL_SW0

        MDL_G1 = (MDL_EE0*(1.000000D+00-MDL_DV/2.000000D+00-MDL_DT
     $   /(2.000000D+00*MDL_SW0__EXP__2)-(MDL_CW0*MDL_DWB)/MDL_SW0))
     $   /MDL_CW0

        MDL_GW = ((1.000000D+00-MDL_DV/2.000000D+00)*MDL_EE0)/MDL_SW0

        MDL_LAM = ((1.000000D+00-MDL_DLAM-MDL_DV)*MDL_MH__EXP__2)
     $   /(2.000000D+00*MDL_VEV0__EXP__2)

        MDL_VEV = (1.000000D+00+MDL_DV/2.000000D+00)*MDL_VEV0

        MDL_EE = (2.000000D+00*MDL_MW*MDL_SW*(1.000000D+00-MDL_DV
     $   /2.000000D+00-(MDL_CW0*MDL_DWB)/MDL_SW0))/MDL_VEV0

        MDL_EE__EXP__2 = MDL_EE**2

        MDL_AEW = MDL_EE__EXP__2/(4.000000D+00*PI)

        AEWM1 = 1.000000D+00/MDL_AEW

        MDL_EE0__EXP__2 = MDL_EE0**2

        MDL_EE0__EXP__3 = MDL_EE0**3

        MDL_VEV0__EXP__3 = MDL_VEV0**3

      ENDIF
C     
C     Parameters that should be recomputed at an event by even basis.
C     
      AS = G**2/4/PI

      MDL_SQRT__AS = SQRT(DCMPLX(AS))

      MDL_G__EXP__2 = G**2

      MDL_G__EXP__3 = G**3

      MDL_G__EXP__4 = G**4

      MDL_MU_R__EXP__2 = MU_R**2

C     
C     Definition of the EW coupling used in the write out of aqed
C     
      GAL(1) = 2.378414230005442133435D0*MDL_MW*DSQRT(1D0-MDL_MW**2
     $ /MDL_MZ**2)*DSQRT(MDL_GF)
      GAL(2) = 1D0

