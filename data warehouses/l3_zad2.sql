CREATE VIEW Lab3Zad2
as
SELECT AdventureWorksLT.SalesLT.Product.ProductID, AdventureWorksLT.SalesLT.Product.Name,
ListPrice, StandardCost, Color,
ListPrice-StandardCost as 'Profit', 100*(ListPrice-StandardCost)/StandardCost as 'Margin',
AdventureWorksLT.SalesLT.ProductCategory.Name as 'Category',
AdventureWorksLT.SalesLT.ProductParentCategory.Name as 'ParentCategory',
IIF(SellEndDate IS NULL, 'True', 'False') as 'Active',
IIF(WeightUnit='LB', Weight*453, Weight) as 'UniWeight',
CASE 
	WHEN AdventureWorksLT.SalesLT.Product.ListPrice>0 and AdventureWorksLT.SalesLT.Product.ListPrice<100 THEN 'Low'
	WHEN AdventureWorksLT.SalesLT.Product.ListPrice>100 and AdventureWorksLT.SalesLT.Product.ListPrice<300 THEN 'Medium'
	WHEN AdventureWorksLT.SalesLT.Product.ListPrice>300 and AdventureWorksLT.SalesLT.Product.ListPrice<500 THEN 'High'
	WHEN AdventureWorksLT.SalesLT.Product.ListPrice>500 THEN 'VeryHigh'
END as 'DiscretePrice',
DATEPART(YEAR, SellStartDate) as 'SSDYear',
DATEPART(QUARTER, SellStartDate) as 'SSDQuarter',
DATEPART(MONTH, SellStartDate) as 'SSDMonth',
DATEPART(DAY, SellStartDate) as 'SSDDay',
DATENAME(MONTH, SellStartDate) as 'SSDMonthName',
IIF(SellEndDate IS NULL, DATEDIFF(YEAR, SellStartDate, GETDATE()),
	DATEDIFF(YEAR, SellStartDate, SellEndDate)) as 'SoldFor',
LEFT(ProductNumber, 2) as 'Type',
SUBSTRING(ProductNumber, 4, 4) as 'Line',
SalesOrderHeader.SalesOrderID, TotalDue, OrderQty,
TotalDue-(OrderQty*StandardCost) as 'OrderProfit'
FROM AdventureWorksLT.SalesLT.Product
INNER JOIN AdventureWorksLT.SalesLT.ProductCategory
ON AdventureWorksLT.SalesLT.Product.ProductCategoryID=AdventureWorksLT.SalesLT.ProductCategory.ProductCategoryID
INNER JOIN AdventureWorksLT.SalesLT.ProductParentCategory
ON AdventureWorksLT.SalesLT.ProductCategory.ParentProductCategoryID=AdventureWorksLT.SalesLT.ProductParentCategory.ProductCategoryID
INNER JOIN AdventureWorksLT.SalesLT.SalesOrderDetail
ON AdventureWorksLT.SalesLT.SalesOrderDetail.ProductID=AdventureWorksLT.SalesLT.Product.ProductID
INNER JOIN AdventureWorksLT.SalesLT.SalesOrderHeader
ON AdventureWorksLT.SalesLT.SalesOrderHeader.SalesOrderID=AdventureWorksLT.SalesLT.SalesOrderDetail.SalesOrderID;