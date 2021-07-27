clear all
set more off
cls

grstyle init
grstyle set plain, horizontal grid

set sformat %8.3f

// cd to your current directory if you run the script from STATA (note that this is automatically handled by regression_analysis.py when running analysis_annual_change.do from main.py)
//cd <path/to/analysis2.do> 

cd "../../data/model"
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

*Correlation (annual change in LS and annual change in MVI)
tsset year
g dsatislfe = satislfe - l.satislfe
g dvalence_md_num1 = valence_md_num1 - l.valence_md_num1
pwcorr dsatislfe dvalence_md_num1, sig

*Scatter (annual change in LS and annual change in MVI)
graph twoway (scatter dsatislfe dvalence_md_num1, mcolor(blue)) (lfit dsatislfe dvalence_md_num1, lcolor(green)), ytitle("Annual change in Life satisfaction") xtitle("Annual change in MVI") legend(off) name("scatter_diff", replace)

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
