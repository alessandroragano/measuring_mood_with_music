clear all
set more off
cls

grstyle init
grstyle set plain, horizontal grid

set sformat %8.3f

*cd "C:\Users\Anthony\Documents\Projects\hm_replication\data"
cd "/Users/alessandroragano/Documents/GitHub/measuring_life_satisfaction_with_music/hm_replication/data"

use "reg_data.dta"
destring year, replace

rename val_score valence
rename lifeexpectanc~l life_exp
rename educatiolineq~e  gini_edu
rename totalgrosscen~a  debt_gov

*Invert the scale of Life satisfaction
replace satislfe = 5-satislfe

*Logarithms
g lgdp = log(rgdpch) // penn GDP
g lvalence_th_av = log(valence_th_av)
g llife_exp = log(life_exp)

*Standardise
egen zsatislfe = std(satislfe)
egen zvalence = std(valence)
egen zvalence_md_num1 = std(valence_md_num1)


// Time Series of LS, MVI and TVI //
label var year "Year"
multiline satislfe valence_md_num1 valence year, mylabels(`" `" "LS " "' `" "MVI" "' `" "TVI" "' "') xline(1980, lcolor(black) lpattern(dash)) xline(1989, lcolor(black) lpattern(dash)) recast(connected) name("time_series", replace) 


// Correlation of LS and MVI //

*Correlation
pwcorr satislfe valence_md_num1, sig

*Scatter
graph twoway (scatter satislfe valence_md_num1, mcolor(blue)) (lfit satislfe valence_md_num1, lcolor(green)), ytitle("Life satisfaction") xtitle("MVI") legend(off) name("scatter", replace)

*Regression 
reg zsatislfe zvalence_md_num1 lgdp year, vce(robust)
reg zsatislfe zvalence_md_num1 lgdp llife_exp gini_edu inflation debt_gov year, vce(robust)


// Comparing MVI and TVI //
reg zsatislfe zvalence_md_num1 zvalence lgdp year, vce(robust)
reg zsatislfe zvalence_md_num1 zvalence lgdp llife_exp gini_edu inflation debt_gov year, vce(robust)


// Comparing MVI with less popular songs //
pwcorr satislfe valence_md_num1, sig
pwcorr satislfe valence_md_num2, sig
pwcorr satislfe valence_md_num3, sig
pwcorr satislfe valence_md_num4, sig
pwcorr satislfe valence_md_num5, sig
pwcorr satislfe valence_md_num6, sig
pwcorr satislfe valence_md_num7, sig
pwcorr satislfe valence_md_num8, sig
pwcorr satislfe valence_md_num9, sig
pwcorr satislfe valence_md_num10, sig
pwcorr satislfe valence_md_av, sig
