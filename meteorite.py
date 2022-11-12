"""Run a linear regression using Apache Spark ML.

In the following PySpark (Spark Python API) code, we take the following actions:

  * Load a previously created linear regression (BigQuery) input table
    into our Cloud Dataproc Spark cluster as an RDD (Resilient
    Distributed Dataset)
  * Transform the RDD into a Spark Dataframe
  * Vectorize the features on which the model will be trained
  * Compute a linear regression using Spark ML

"""
from pyspark.context import SparkContext
from pyspark.ml.linalg import Vectors
from pyspark.ml.regression import LinearRegression
from pyspark.sql.session import SparkSession
# The imports, above, allow us to access SparkML features specific to linear
# regression as well as the Vectors types.


# Define a function that collects the features of interest
# (mother_age, father_age, and gestation_weeks) into a vector.
# Package the vector in a tuple containing the label (`weight_pounds`) for that
# row.
def vector_from_inputs(r):
  return (r["mass__g_"], Vectors.dense(float(r["reclat"]),

                                            float(r["reclong"])))

sc = SparkContext()
spark = SparkSession(sc)

# Read the data from BigQuery as a Spark Dataframe.
masscoor_data = spark.read.format("bigquery").option(
    "table", "meteorite.mass_coor").load()
# Create a view so that Spark SQL queries can be run against the data.
masscoor_data.createOrReplaceTempView("masscoorview")

# As a precaution, run a query in Spark SQL to ensure no NULL values exist.
sql_query = """
SELECT *
from masscoorview

"""
clean_data = spark.sql(sql_query)


print("this is to show the result of the clean data of sql query")
#print(clean_data)

# Create an input DataFrame for Spark ML using the above function.
training_data = clean_data.rdd.map(vector_from_inputs).toDF(["label",
                                                             "features"])




print("this is the result of the training data after cache() and the count() of data")

t = training_data.cache()

print(t.count())

# Construct a new LinearRegression object and fit the training data.
lr = LinearRegression(maxIter=5, regParam=0.2, solver="normal")



print("test log 1")

model = lr.fit(training_data)
# Print the model summary.
print("Coefficients:" + str(model.coefficients))
print("Intercept:" + str(model.intercept))
print("R^2:" + str(model.summary.r2))
model.summary.residuals.show()

