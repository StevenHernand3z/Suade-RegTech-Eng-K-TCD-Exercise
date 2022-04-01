import json
import datetime
    
def calculator(datajson):    
    with open(datajson) as file:
        transactionlegs = json.load(file)

    #============================================================================
    #First establish customer type, below is a code to get customer type but 
    #it is very difficult to compare types without a limited type of entities
    #so below is a list where we can add any type of counterparty that
    #would be classed as a central bank, central government, public sector entity,
    #credit institution or investment firm
    #============================================================================
    
    
    listofentities = ['central_bank','regional_govt','central_govt','regional_bank'
                      ,'investment_firm']
    
    
    #============================================================================
    #This is to determine the Risk Factor as determined in 
    #table 2 of article 26 (page 314/31)
    #============================================================================
    
    if (transactionlegs.get("data")[0].get("customer").get("type") in listofentities) == True:
        RF = 0.016
    else:
        RF = 0.08
        
    
    #============================================================================
    #Next we will establish the exposure value
    
    #EV is the maximum between 0 and the replacement cost (RC) + potential future
    #exposure (PFE - not relevant for Repos) - collateral (C)
    #============================================================================
    
    
    #RC value is defined as the cash balance for a reverse repo
    
    
    if transactionlegs.get("data")[0].get("id")=="rev_repo_cash_leg":
        RC = abs(transactionlegs.get("data")[0].get("balance"))
    elif transactionlegs.get("data")[1].get("id")=="rev_repo_cash_leg":
        RC = abs(transactionlegs.get("data")[1].get("balance"))
    
    
    if transactionlegs.get("data")[0].get("id")=="rev_repo_asset_leg":
        C = transactionlegs.get("data")[0].get("mtm_dirty")
    elif transactionlegs.get("data")[1].get("id")=="rev_repo_asset_leg":
        C = transactionlegs.get("data")[1].get("mtm_dirty")
        
    EV = max(RC-C,0)
    
    
    #============================================================================
    
    #This commented section of code determines the length of time between the repo
    #dates. This could be required if determining whether or not this is a long
    #settlement transaction.
    
    #============================================================================
    
    # year1 = int(transactionlegs.get("data")[0].get("date")[0:4])
    # month1 = int(transactionlegs.get("data")[0].get("date")[5:7])
    # day1 = int(transactionlegs.get("data")[0].get("date")[8:10])
    
    # year2 = int(transactionlegs.get("data")[0].get("end_date")[0:4])
    # month2 = int(transactionlegs.get("data")[0].get("end_date")[5:7])
    # day2 = int(transactionlegs.get("data")[0].get("end_date")[8:10])
    
    # daydiff = (datetime.datetime(year2,month2,day2)-datetime.datetime(year1,month1,day1)).days
    
    
    CVA = 1.5
    
    
    #Here we have to test if the counterparty is a non-financial entity
    #As per Article 2 of Regulation (EU) No 648/2012 point (1) we have classed a government
    #to be a financial counterparty
    
    if (transactionlegs.get("data")[0].get("customer").get("type") in listofentities) == True:
        CVA = 1
    
    #Here we are comparing the customer ID and issuer ID to see if this is an 
    #intragroup transaction (assuming for intragroup transactions they use the same ID)
    
    if transactionlegs.get("data")[0].get("customer_id") is not None:
        if transactionlegs.get("data")[0].get("issuer_id") is not None:
            if transactionlegs.get("data")[0].get("customer_id").get('type')==transactionlegs.get("data")[0].get("issuer_id").get('type'):
                CVA = 1
    
    
    if transactionlegs.get("data")[1].get("customer_id") is not None:
        if transactionlegs.get("data")[1].get("issuer_id") is not None:
            if transactionlegs.get("data")[1].get("customer_id").get('type')==transactionlegs.get("data")[1].get("issuer_id").get('type'):
                CVA = 1
    
    
    
    KTCD = 1.2*EV*RF*CVA

    return KTCD

   #============================================================================
   #Unit Testing
   #verify duration
   #============================================================================
