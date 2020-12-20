#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/5 12:38 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : ths_test.py
# @Software: PyCharm
from pprint import pprint as show
# --- Evolving
# -----------------------------------------
from common.ths_utils import Service, Evolving

service = Service()
status = service.loginClient()
print("service:", status)
#
dw = Evolving()
dw.keepInformed = True
#
bids = dw.getBids(stockCode="000002")
show(bids)

# status = dw.isBrokerLoggedIn()
# print(status)

# status = dw.loginBroker()
# print(status)

# status = dw.isBrokerLoggedIn()
# print(status)

# accountInfo = dw.getAccountInfo()
# show(accountInfo)

# status = dw.transfer(transferType = "broker2bank", amount = 1000)
# show(status)

# status = dw.transfer(transferType = "bank2broker", amount = 1000)
# show(status)

# status = dw.transfer_broker2bank(amount = 10000)
# show(status)

# status = dw.transfer_bank2broker(amount = 10000)
# show(status)

# transferRecords = dw.getTransferRecords(dateRange="thisYear")
# show(transferRecords)



# bids = dw.getBids(stockCode = "600030", assetType = 'stock')
# show(bids)

# bids = dw.getBids(stockCode = "688055")
# show(bids)
# bids = dw.getBids(stockCode = "688055", assetType = 'sciTech')
# show(bids)

# bids = dw.getBids(stockCode = "300750", assetType = 'gem')
# show(bids)
# bids = dw.getBids(stockCode = "300750")
# show(bids)

# status, contractNo = dw.issuingEntrust(stockCode = '002241', amount = 100, price = 37.01, tradingAction = 'buy')
# show(status)
# show(contractNo)
# status, contractNo = dw.issuingEntrust(stockCode = '002241', amount = 100, price = 40.01, tradingAction = 'sell')
# show(status)
# show(contractNo)
# status, contractNo = dw.issuingEntrust(stockCode = '002241', amount = 100, tradingAction = 'buy')

# show(status)
# show(contractNo)
# status, contractNo = dw.issuingEntrust(stockCode = '002241', amount = 100, tradingAction = 'sell')
# show(status)
# show(contractNo)

# status, contractNo = dw.issuingEntrust(stockCode = '688050', amount = 200, price = 220.01, tradingAction = 'buy')
# show(status)
# show(contractNo)
# status, contractNo = dw.issuingEntrust(stockCode = '688050', amount = 200, price = 225.01, tradingAction = 'sell')
# show(status)
# show(contractNo)
# status, contractNo = dw.issuingEntrust(stockCode = '688050', amount = 200, tradingAction = 'buy')
# show(status)
# show(contractNo)
# status, contractNo = dw.issuingEntrust(stockCode = '688050', amount = 200, tradingAction = 'sell')
# show(status)
# show(contractNo)

# status, contractNo = dw.issuingEntrust(stockCode = '300474', amount = 200, price = 72.54, tradingAction = 'buy')
# show(status)
# show(contractNo)
# status, contractNo = dw.issuingEntrust(stockCode = '300474', amount = 200, price = 78.41, tradingAction = 'sell')
# show(status)
# show(contractNo)
# status, contractNo = dw.issuingEntrust(stockCode = '300474', amount = 200, tradingAction = 'buy')
# show(status)
# show(contractNo)
# status, contractNo = dw.issuingEntrust(stockCode = '300474', amount = 200, tradingAction = 'sell')
# show(status)
# show(contractNo)

# status, contractNo = dw.buy(stockCode = '002241', amount = 100)
# show(status)
# show(contractNo)
# status, contractNo = dw.buy(stockCode = '002241', amount = 100, price = 37.01)
# show(status)
# show(contractNo)
# status, contractNo = dw.buy(stockCode = '688050', amount = 200, price = 220.01)
# show(status)
# show(contractNo)
# status, contractNo = dw.buy(stockCode = '300474', amount = 200, price = 72.54)
# show(status)
# show(contractNo)

# status, contractNo = dw.sell(stockCode = '002241', amount = 100)
# show(status)
# show(contractNo)
# status, contractNo = dw.sell(stockCode = '002241', amount = 100, price = 37.01)
# show(status)
# show(contractNo)
# status, contractNo = dw.sell(stockCode = '688050', amount = 200, price = 220.01)
# show(status)
# show(contractNo)
# status, contractNo = dw.sell(stockCode = '300474', amount = 200, price = 72.54)
# show(status)
# show(contractNo)

# status, contractNo = dw.buyStock(stockCode = '002241', amount = 100, price = 37.01)
# show(status)
# show(contractNo)
# status, contractNo = dw.sellStock(stockCode = '002241', amount = 100, price = 40.01)
# show(status)
# show(contractNo)
# status, contractNo = dw.buyStock(stockCode = '002241', amount = 100)
# show(status)
# show(contractNo)
# status, contractNo = dw.sellStock(stockCode = '002241', amount = 100)
# show(status)
# show(contractNo)

# status, contractNo = dw.buySciTech(stockCode = '688050', amount = 200, price = 225.01)
# show(status)
# show(contractNo)
# status, contractNo = dw.sellSciTech(stockCode = '688050', amount = 200, price = 220.01)
# show(status)
# show(contractNo)
# status, contractNo = dw.buySciTech(stockCode = '688050', amount = 200)
# show(status)
# show(contractNo)
# status, contractNo = dw.sellSciTech(stockCode = '688050', amount = 200)
# show(status)
# show(contractNo)

# status, contractNo = dw.buyGem(stockCode = '300474', amount = 200, price = 72.54)
# show(status)
# show(contractNo)
# status, contractNo = dw.sellGem(stockCode = '300474', amount = 200, price = 78.41)
# show(status)
# show(contractNo)
# status, contractNo = dw.buyGem(stockCode = '300474', amount = 200)
# show(status)
# show(contractNo)
# status, contractNo = dw.sellGem(stockCode = '300474', amount = 200)
# show(status)
# show(contractNo)

# todayIPO = dw.getTodayIPO()
# show(todayIPO)

# status = dw.oneKeyIPO()
# print(status)

# status = dw.revokeEntrust(revokeType = "allBuyAndSell", assetType = "stock", contractNo = None)
# show(status)
# status = dw.revokeEntrust(revokeType = "allBuy", assetType = "stock", contractNo = None)
# show(status)
# status = dw.revokeEntrust(revokeType = "allSell", assetType = "stock", contractNo = None)
# show(status)

# # note: brew install cliclick
# status = dw.revokeContractNoEntrust(assetType = "stock",  contractNo = "N8536587")
# show(status)

# status = dw.revokeAllEntrust()
# show(status)
# status = dw.revokeAllBuyEntrust()
# show(status)
# status = dw.revokeAllSellEntrust()
# show(status)

# holdingShares = dw.getHoldingShares(assetType = 'stock')
# show(holdingShares)

# allholdingShares = dw.getAllHoldingShares()
# show(allholdingShares)

# entrust = dw.getEntrust(assetType = 'stock', dateRange = 'today', isRevocable = True)
# show(entrust)

# entrust = dw.getEntrust(assetType = 'stock', dateRange = 'today', isRevocable = False)
# show(entrust)

# entrust = dw.getEntrust(assetType = 'stock', dateRange = 'thisWeek', isRevocable = False)
# show(entrust)
# print(len(entrust.get('data')))

# entrust = dw.getEntrust(assetType = 'stock', dateRange = 'thisYear', isRevocable = False)
# show(entrust)

# res = dw.getTodayAllRevocableEntrust()
# show(res)

# closedDeals = dw.getClosedDeals(assetType = 'stock', dateRange = 'thisSeason')
# show(closedDeals)

# closedDeals = dw.getClosedDeals(assetType = 'stock', dateRange = 'today')
# show(closedDeals)

# capitalDetails = dw.getCapitalDetails(assetType = 'stock', dateRange = 'thisSeason')
# show(capitalDetails)

# capitalDetails = dw.getCapitalDetails(assetType = 'stock', dateRange = 'today')
# show(capitalDetails)

# res = dw.getIPO(queryType = "entrust", dateRange = "today")
# show(res)

# # this line will be fail
# res = dw.getIPO(queryType = "entrust", dateRange = "thisWeek")
# show(res)

# res = dw.getIPO(queryType = "allotmentNo", dateRange = "thisMonth")
# show(res)

# res = dw.getIPO(queryType = "winningLots", dateRange = "thisSeason")
# show(res)

# status = dw.liquidating()
# show(status)

# StockCodeAmountPriceList = [['512290', '1000', '2.169'], ['512290', '1000', '2.171'], ['688050', '200', '225.01']]
# statusList = dw.entrustPortfolio(StockCodeAmountPriceList)
# show(statusList)

# status = dw.revokeAllEntrust()
# show(status)

# service.logoutClient()

# --- EvolvingSim
# -----------------------------------------
# service = Service()

# status = service.loginClient()
# print(status)
# time.sleep(3)

# dws = EvolvingSim()

# simulationAccountInfo = dws.getAccountInfo()
# show(simulationAccountInfo)

# status, contractNo = dws.issuingEntrust(stockCode = '002241', amount = 100, price = 37.01, tradingAction = 'buy')
# show(status)
# show(contractNo)
# status, contractNo = dws.issuingEntrust(stockCode = '600196', amount = 100, price = 60.01, tradingAction = 'buy')
# show(status)
# show(contractNo)
# status, contractNo = dws.issuingEntrust(stockCode = '600196', amount = 100, tradingAction = 'buy')
# show(status)
# show(contractNo)
# status, contractNo = dws.issuingEntrust(stockCode = '600196', amount = 100, price = 61.81, tradingAction = 'sell')
# show(status)
# show(contractNo)
# status, contractNo = dws.issuingEntrust(stockCode = '002241', amount = 200, price = 40.01, tradingAction = 'sell')
# show(status)
# show(contractNo)
# status, contractNo = dws.issuingEntrust(stockCode = '002241', amount = 200, tradingAction = 'sell')
# show(status)
# show(contractNo)

# res = dws.revokeEntrust(revokeType = "allBuyAndSell", contractNo = None)
# show(res)
# res = dws.revokeEntrust(revokeType = "allBuy", contractNo = None)
# show(res)
# res = dws.revokeEntrust(revokeType = "allSell", contractNo = None)
# show(res)
# res = dws.revokeEntrust(revokeType = "contractNo", contractNo = "1670247753")
# show(res)

# simulationHoldingShares = dws.getHoldingShares()
# show(simulationHoldingShares)

# simulationEntrustment = dws.getEntrust(dateRange = 'today', isRevocable = False)
# show(simulationEntrustment)

# simulationEntrustment = dws.getEntrust(dateRange = 'today', isRevocable = True)
# show(simulationEntrustment)

# simulationClosedDeals = dws.getClosedDeals(dateRange = 'today')
# show(simulationClosedDeals)

# simulationClosedDeals = dws.getClosedDeals(dateRange = 'thisMonth')
# show(simulationClosedDeals)

# simulationCapitalDetails = dws.getCapitalDetails(dateRange = 'today')
# show(simulationCapitalDetails)

# simulationCapitalDetails = dws.getCapitalDetails(dateRange = 'thisMonth')
# show(simulationCapitalDetails)

# status = dws.liquidating()
# show(status)

# StockCodeAmountPriceList = [['512290', '1000', '2.169'], ['512290', '1000', None]]
# res = dws.entrustPortfolio(StockCodeAmountPriceList)
# show(res)

# status = service.logoutClient()
# print(status)
