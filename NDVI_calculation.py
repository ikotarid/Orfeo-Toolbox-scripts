
import otbApplication

# 3. Compute radiometric indices - NDVI (NIR-R)/(R+NIR)
app = otbApplication.Registry.CreateApplication("RadiometricIndices")
app.SetParameterString("in", r"C:\.....\abc.tif")#set stacked image path
app.SetParameterStringList("list", ["Vegetation:NDVI"])
app.SetParameterInt("channels.red", 3)
app.SetParameterInt("channels.nir", 7)
app.SetParameterString("out", r"C:\....")#set output path
app.ExecuteAndWriteOutput()
