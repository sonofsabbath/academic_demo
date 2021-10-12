CREATE VIEW Lab3Zad4
as
SELECT SalesOrderHeader.SalesOrderID, OrderDate, DATEPART(YEAR, OrderDate) as 'OrderYear',
DATEPART(MONTH, OrderDate) as 'OrderMonth', DATEPART(DAY, OrderDate) as 'OrderDay',
FirstName, LastName, CompanyName,
City, StateProvince, CountryRegion,
TotalDue, OrderQty
FROM AdventureWorksLT.SalesLT.SalesOrderHeader
INNER JOIN AdventureWorksLT.SalesLT.Customer
ON SalesOrderHeader.CustomerID=Customer.CustomerID
INNER JOIN AdventureWorksLT.SalesLT.Address
ON SalesOrderHeader.ShipToAddressID=Address.AddressID
INNER JOIN AdventureWorksLT.SalesLT.SalesOrderDetail
ON SalesOrderDetail.SalesOrderID=SalesOrderHeader.SalesOrderID;