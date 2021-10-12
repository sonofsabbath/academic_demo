USE AdventureWorksLT;   
GO 
 
CREATE VIEW Wzgledem_czasu
AS
SELECT D3.OrderDate
,D1.ProductID
,D3.SalesOrderID
,DATEPART(year, D3.[OrderDate]) "OrderYear"
,DATEPART(quarter, D3.[OrderDate]) "OrderQuarter"
,DATEPART(month, D3.[OrderDate]) "OrderMonth"
,DATEPART(week, D3.[OrderDate]) "OrderWeek"
,DATEPART(day, D3.[OrderDate]) "OrderDay"
,DATEPART(weekday, D3.[OrderDate]) "SSDWeekDay"
FROM [AdventureWorksLT].[SalesLT].[Product] "D1" 
JOIN [AdventureWorksLT].[SalesLT].[SalesOrderDetail] "D2" ON D1.ProductID=D2.ProductID
JOIN [AdventureWorksLT].[SalesLT].[SalesOrderHeader] "D3" ON D2.SalesOrderID=D3.SalesOrderID
JOIN [AdventureWorksLT].[SalesLT].[ProductCategory] "D4" ON D1.ProductCategoryID=D4.ProductCategoryID
JOIN [AdventureWorksLT].[SalesLT].[ProductParentCategory] "D5" ON D4.ParentProductCategoryID=D5.ProductCategoryID
JOIN [AdventureWorksLT].[SalesLT].[Customer] "D6" ON D3.CustomerID=D6.CustomerID
JOIN [AdventureWorksLT].[SalesLT].[CustomerAddress] "D7" ON D6.CustomerID=D7.CustomerID
JOIN [AdventureWorksLT].[SalesLT].[Address] "D8" ON D7.AddressID=D8.AddressID
JOIN [AdventureWorksLT].[SalesLT].[SalesPerson] "D9" ON D6.SalesPersonID=D9.SalesPersonID


USE AdventureWorksLT;   
GO 
CREATE VIEW Wzgledem_produktu
AS
SELECT D1.ProductID, D1.ProductCategoryID, D1.Name, D4.Name "CategoryName", D4.ParentProductCategoryID, D5.Name "ParentCategoryName"
FROM [AdventureWorksLT].[SalesLT].[Product] "D1" 
JOIN [AdventureWorksLT].[SalesLT].[SalesOrderDetail] "D2" ON D1.ProductID=D2.ProductID
JOIN [AdventureWorksLT].[SalesLT].[SalesOrderHeader] "D3" ON D2.SalesOrderID=D3.SalesOrderID
JOIN [AdventureWorksLT].[SalesLT].[ProductCategory] "D4" ON D1.ProductCategoryID=D4.ProductCategoryID
JOIN [AdventureWorksLT].[SalesLT].[ProductParentCategory] "D5" ON D4.ParentProductCategoryID=D5.ProductCategoryID
JOIN [AdventureWorksLT].[SalesLT].[Customer] "D6" ON D3.CustomerID=D6.CustomerID
JOIN [AdventureWorksLT].[SalesLT].[CustomerAddress] "D7" ON D6.CustomerID=D7.CustomerID
JOIN [AdventureWorksLT].[SalesLT].[Address] "D8" ON D7.AddressID=D8.AddressID
JOIN [AdventureWorksLT].[SalesLT].[SalesPerson] "D9" ON D6.SalesPersonID=D9.SalesPersonID

/*WHERE D1.ProductID IS NULL OR D1.ProductCategoryID IS NULL OR D1.Name IS NULL OR D4.Name IS NULL OR D4.ParentProductCategoryID IS NULL OR D5.Name IS NULL OR*/

CREATE VIEW Wzgledem_klienta
AS
SELECT D7.AddressID
,D6.CustomerID 
,(SELECT CASE 
			WHEN COUNT(D.SalesOrderID)<=4 THEN 'Occasional'
			WHEN 4<COUNT(D.SalesOrderID) AND COUNT(D.SalesOrderID)<=8 THEN 'Regular'  
			WHEN 8<COUNT(D.SalesOrderID) THEN 'Frequent'
			END "ClientType"
		FROM [AdventureWorksLT].[SalesLT].[SalesOrderHeader] "D"
		WHERE D.CustomerID=D6.CustomerID
		GROUP BY D.CustomerID) "ClientType"
,D8.City
,D8.StateProvince
,D8.CountryRegion
FROM [AdventureWorksLT].[SalesLT].[Product] "D1" 
JOIN [AdventureWorksLT].[SalesLT].[SalesOrderDetail] "D2" ON D1.ProductID=D2.ProductID
JOIN [AdventureWorksLT].[SalesLT].[SalesOrderHeader] "D3" ON D2.SalesOrderID=D3.SalesOrderID
JOIN [AdventureWorksLT].[SalesLT].[ProductCategory] "D4" ON D1.ProductCategoryID=D4.ProductCategoryID
JOIN [AdventureWorksLT].[SalesLT].[ProductParentCategory] "D5" ON D4.ParentProductCategoryID=D5.ProductCategoryID
JOIN [AdventureWorksLT].[SalesLT].[Customer] "D6" ON D3.CustomerID=D6.CustomerID
JOIN [AdventureWorksLT].[SalesLT].[CustomerAddress] "D7" ON D6.CustomerID=D7.CustomerID
JOIN [AdventureWorksLT].[SalesLT].[Address] "D8" ON D7.AddressID=D8.AddressID
JOIN [AdventureWorksLT].[SalesLT].[SalesPerson] "D9" ON D6.SalesPersonID=D9.SalesPersonID

CREATE VIEW miary_dot_sprzedazy
AS
SELECT D3.SalesOrderID, D6.CustomerID, D1.ProductID, D7.AddressID, D2.OrderQty
,(D2.[UnitPrice]*(1-D2.[UnitPriceDiscount]))*D2.OrderQty "SaleValue"
,(D2.[UnitPrice]*(1-D2.[UnitPriceDiscount])-D1.StandardCost)*D2.OrderQty "Profit"
,D3.ShipToAddressID, D3.TaxAmt
FROM [AdventureWorksLT].[SalesLT].[Product] "D1" 
JOIN [AdventureWorksLT].[SalesLT].[SalesOrderDetail] "D2" ON D1.ProductID=D2.ProductID
JOIN [AdventureWorksLT].[SalesLT].[SalesOrderHeader] "D3" ON D2.SalesOrderID=D3.SalesOrderID
JOIN [AdventureWorksLT].[SalesLT].[ProductCategory] "D4" ON D1.ProductCategoryID=D4.ProductCategoryID
JOIN [AdventureWorksLT].[SalesLT].[ProductParentCategory] "D5" ON D4.ParentProductCategoryID=D5.ProductCategoryID
JOIN [AdventureWorksLT].[SalesLT].[Customer] "D6" ON D3.CustomerID=D6.CustomerID
JOIN [AdventureWorksLT].[SalesLT].[CustomerAddress] "D7" ON D6.CustomerID=D7.CustomerID
JOIN [AdventureWorksLT].[SalesLT].[Address] "D8" ON D7.AddressID=D8.AddressID
JOIN [AdventureWorksLT].[SalesLT].[SalesPerson] "D9" ON D6.SalesPersonID=D9.SalesPersonID


--Zadanie2_raport1
--która grupa klientów generuje wiêkszy zysk- globalnie
SELECT TOP 1 D1.ClientType, 
SUM(D2.SaleValue) "MAXI"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
GROUP BY D1.ClientType
ORDER BY MAXI
DESC

--która grupa klientów generuje wiêkszy zysk - w ujêciu czasowym
SELECT TOP 1 D1.ClientType, D3.SSDYear, D3.SSDMonth,
SUM(D2.SaleValue) "MAXI"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
JOIN [AdventureWorksLT].[dbo].[Wzgledem_czasu] "D3" ON D3.ProductID=D2.ProductID
GROUP BY D1.ClientType, D3.SSDYear, D3.SSDMonth
ORDER BY MAXI
DESC

--10 najlepszych klientów

SELECT TOP 10 D1.CustomerID, SUM(D2.SaleValue) "ClientValue"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
GROUP BY D1.CustomerID
ORDER BY "ClientValue"
DESC


--Najgorszych lokalizacji klientów

SELECT D1.AddressID, SUM(D2.SaleValue) "AddressValue"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
GROUP BY D1.AddressID
ORDER BY "AddressValue"
ASC

/*Zadanie2_raport2*/

--najlepszy miesi¹c

SELECT TOP 1 D3.SSDMonth,
AVG(D2.SaleValue) "Globa"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
JOIN [AdventureWorksLT].[dbo].[Wzgledem_czasu] "D3" ON D3.ProductID=D2.ProductID
GROUP BY D3.SSDMonth
ORDER BY Globa
DESC

--najgorszy miesi¹c

SELECT TOP 1 D3.SSDMonth,
AVG(D2.SaleValue) "Globa"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
JOIN [AdventureWorksLT].[dbo].[Wzgledem_czasu] "D3" ON D3.ProductID=D2.ProductID
GROUP BY D3.SSDMonth
ORDER BY Globa
ASC

--najlepszy miesi¹c w poszczególnych latch

SELECT TOP 1 D3.SSDYear, D3.SSDMonth,
SUM(D2.SaleValue) "Best"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
JOIN [AdventureWorksLT].[dbo].[Wzgledem_czasu] "D3" ON D3.ProductID=D2.ProductID
GROUP BY D3.SSDYear, D3.SSDMonth
ORDER BY Best
DESC

--najgorszy miesi¹c w poszczególnych latch

SELECT TOP 1 D3.SSDYear, D3.SSDMonth,
SUM(D2.SaleValue) "Worst"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
JOIN [AdventureWorksLT].[dbo].[Wzgledem_czasu] "D3" ON D3.ProductID=D2.ProductID
GROUP BY D3.SSDYear, D3.SSDMonth
ORDER BY Worst
ASC

--najpopularniejszy dzieñ tygodnia

SELECT TOP 1 D3.SSDWeekDay,
AVG(D2.SaleValue) "BestDay"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
JOIN [AdventureWorksLT].[dbo].[Wzgledem_czasu] "D3" ON D3.ProductID=D2.ProductID
GROUP BY D3.SSDWeekDay
ORDER BY BestDay
DESC

/*Zadanie2_raport3*/

--najlepszy miesi¹c dla danej kategorii produktów 

SELECT TOP 1 D3.SSDYear, D3.SSDMonth,
SUM(D2.SaleValue) "Best"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
JOIN [AdventureWorksLT].[dbo].[Wzgledem_czasu] "D3" ON D3.ProductID=D2.ProductID
GROUP BY D3.SSDYear, D3.SSDMonth
ORDER BY Best
DESC

SELECT TOP 1 D3.SSDYear, D3.SSDMonth,
SUM(D2.SaleValue) "Best"
FROM [AdventureWorksLT].[dbo].[Wzgledem_klienta] "D1"
JOIN [AdventureWorksLT].[dbo].[miary_dot_sprzedazy] "D2" ON D1.AddressID=D2.AddressID
JOIN [AdventureWorksLT].[dbo].[Wzgledem_czasu] "D3" ON D3.ProductID=D2.ProductID
GROUP BY D3.SSDYear, D3.SSDMonth
ORDER BY Best
DESC
--Najgorszy miesi¹c dla danej kategorii produktów 