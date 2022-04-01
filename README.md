## Trading Counterparty Default Risk (K-TCD) Calculator
This project is a simple Trading Counterparty Default Risk (K-TCD) calculator, created in Python.

## Table of Contents
* [General Information](#general-information)
* [K-TCD Computation](#k-tdc-computation)
* [Technologies](#technologies)
* [Launch](#launch)

## General Information
This calculator computes the K-TCD value for Reverse Repo transactions, specifically a two legged Securities Financing Transaction (SFT). All in accordance with Chapter 4 Section 1 "Trading Counterparty default" in the Investment Firm Regulation [Link](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32019R2033) (Articles 26-32).

## K-TCD Computation

 K-TDC = α * EV * RF * CVA

where:

* α = 1.2 
* EV = the exposure value, as defined in Article 27 
* RF = the risk factor per counterparty type, as defined in Article 26, Table 2 
* CVA = the credit valuation adjustment, as defined in Article 32

## Technologies
Project is created with:

* Python Version: 3.9
* Numpy
* Json

## Launch
The algorithm accepts as it's input a JSON file (.json) conforming to the FIRE Data Format [Link](https://github.com/suadelabs/fire), and that is saved in the same directory as it's code.
