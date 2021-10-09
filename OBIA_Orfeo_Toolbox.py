#1. Resample 20m bands to 10m
app = otbApplication.Registry.CreateApplication("RigidTransformResample")
app.SetParameterString("in", "Path of input image")
app.SetParameterString("out", "Path of output image")
app.SetParameterString("transform.type","id")
app.SetParameterFloat("transform.type.id.scalex", 2.0)
app.SetParameterFloat("transform.type.id.scaley", 2.0)
app.SetParameterString("interpolator","nn")
app.SetParameterOutputImagePixelType("out", 2) # Uint16
app.ExecuteAndWriteOutput()

#2a. Crop bands to AOI
app = otbApplication.Registry.CreateApplication("ExtractROI")
app.SetParameterString("in", "Path of input image")
app.SetParameterString("mode","fit")
app.SetParameterFloat("mode.fit.vect", "Path of vector file")
app.SetParameterString("out", "Path of output image")
app.ExecuteAndWriteOutput()

#2b. Crop bands to lower-left XY and upper-right XY! UTM PROJ
app = otbApplication.Registry.CreateApplication("ExtractROI")
app.SetParameterString("in", "Path of input image")
app.SetParameterString("mode","extent")
app.SetParameterFloat("mode.extent.ulx", 550966)
app.SetParameterFloat("mode.extent.uly", 4490113)
app.SetParameterFloat("mode.extent.lrx", 558523)
app.SetParameterFloat("mode.extent.lry", 4499870)
app.SetParameterString("mode.extent.unit", "lonlat")
app.SetParameterString("out", "Path of output image")
app.SetParameterOutputImagePixelType("out", 2) # Uint16
app.ExecuteAndWriteOutput()

#3. Stack bands
app = otbApplication.Registry.CreateApplication("ConcatenateImages")
app.SetParameterStringList("il", ['image_1','image_2',...,'image_n'])
app.SetParameterString("out",r"Path of output image")
app.SetParameterOutputImagePixelType("out", 2) # Uint16
app.ExecuteAndWriteOutput()

# 4. Segmentation: Performs segmentation of an image, and outputs a vector file.
app = otbApplication.Registry.CreateApplication("Segmentation")
app.SetParameterString("in", "image file")
app.SetParameterString("mode","vector")
app.SetParameterString("mode.vector.out", "Output vector file")
app.SetParameterString("filter","Segmentation algorithm")

#set algorithm parameters

app.SetParameterString("mode.vector.neighbor", "true")
app.ExecuteAndWriteOutput()

# 5. ZonalStatistics: This application computes zonal statistics
app = otbApplication.Registry.CreateApplication("ZonalStatistics")
app.SetParameterString("in", "image file")
app.SetParameterString("inzone.vector.in", "Segmentation output vector file")
app.SetParameterString("out.vector.filename", "Output vector file with zonal statistics")
app.ExecuteAndWriteOutput()

# 6. TrainVectorClassifier: Train a classifier based on labeled geometries and a list of features to consider
app = otbApplication.Registry.CreateApplication("TrainVectorClassifier")
app.SetParameterStringList("io.vd", ["Training vector file"])
app.SetParameterString("io.out", "Output training model")
app.SetParameterStringList("feat", ["List of field names in the input vector data to be used as features for training"])
app.SetParameterStringList("cfield", ["Field containing the class integer label for supervision"])
app.SetParameterString("classifier.libsvm.opt", "true")
app.ExecuteAndWriteOutput()

# 7. VectorClassifier: Performs a classification of the input vector data according to a model file
app = otbApplication.Registry.CreateApplication("VectorClassifier")
app.SetParameterString("in", "Vector file with zonal statistics")
app.SetParameterString("model", "Training model")
app.SetParameterString("out", "Output classified Vector file")
app.SetParameterStringList("feat", ["List of field names in the input vector data used as features for training.\
                                   The same field names as the TrainVectorClassifier application"])
app.SetParameterString("cfield", "Field containing the predicted class")
app.ExecuteAndWriteOutput()
