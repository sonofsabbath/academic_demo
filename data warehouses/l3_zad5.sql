CREATE VIEW Lab3Zad5
as
SELECT Product.ProductID, Product.Name, Product.Color, Product.StandardCost,
ProductCategory.Name as 'Category', ProductParentCategory.Name as 'ParentCategory',
FirstName+' '+LastName as 'ClientName',
(SELECT CASE
		WHEN COUNT(D.SalesOrderID)<4 THEN 'Occasional'
		WHEN COUNT(D.SalesOrderID)>=4 and COUNT(D.SalesOrderID)<8 THEN 'Regular'
		WHEN COUNT(D.SalesOrderID)>=8 THEN 'Frequent'
		END
 FROM AdventureWorksLT.SalesLT.SalesOrderHeader "D"
 WHERE D.CustomerID=D3.CustomerID
 GROUP BY D.CustomerID) as 'ClientType',
City, StateProvince, CountryRegion,
DATEPART(YEAR, D3.OrderDate) as 'OrderYear',
DATEPART(QUARTER, D3.OrderDate) as 'OrderQuarter',
DATEPART(MONTH, D3.OrderDate) as 'OrderMonth',
DATEPART(DAY, D3.OrderDate) as 'OrderDay',
DATEPART(WEEKDAY, D3.OrderDate) as 'OrderWeekday',
TotalDue, OrderQty, UnitPrice-StandardCost as 'Profit'
FROM AdventureWorksLT.SalesLT.Product --D1
JOIN AdventureWorksLT.SalesLT.SalesOrderDetail --D2
ON Product.ProductID=SalesOrderDetail.ProductID
JOIN AdventureWorksLT.SalesLT.SalesOrderHeader "D3"
ON SalesOrderDetail.SalesOrderID=D3.SalesOrderID
JOIN AdventureWorksLT.SalesLT.ProductCategory --D4
ON Product.ProductCategoryID=ProductCategory.ProductCategoryID
JOIN AdventureWorksLT.SalesLT.ProductParentCategory --D5
ON ProductCategory.ParentProductCategoryID=ProductParentCategory.ProductCategoryID
JOIN AdventureWorksLT.SalesLT.Customer --D6
ON D3.CustomerID=Customer.CustomerID
JOIN AdventureWorksLT.SalesLT.CustomerAddress --D7
ON CustomerAddress.CustomerID=Customer.CustomerID
JOIN AdventureWorksLT.SalesLT.Address --D8
ON CustomerAddress.AddressID=Address.AddressID;