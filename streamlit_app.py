import streamlit as st 
import torch
from PIL import Image
from prediction import pred_class
import numpy as np

# Set title 
st.title('Tomato Leaf Classification')
#Set Header 
st.header('Please up load picture')


#Load Model 
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = torch.load('mobilenetv3_large_100_checkpoint_fold0.pt', map_location=device)
# model = model.to(torch.float32)



# Display image & Prediction 
uploaded_image = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'])

if uploaded_image is not None:
    image = Image.open(uploaded_image).convert('RGB')
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    class_name = ['Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold', 'Septoria_leaf_spot',
               'Spider_Mites', 'Target_Spot', 'Yellow_Leaf_Curl_Virus', 'healthy', 'mosaic_virus']

    if st.button('Prediction'):
        #Prediction class
        probli = pred_class(model,image,class_name)
        
        st.write("## Prediction Result")
        # Get the index of the maximum value in probli[0]
        max_index = np.argmax(probli[0])

        # Iterate over the class_name and probli lists
        for i in range(len(class_name)):
            # Set the color to blue if it's the maximum value, otherwise use the default color
            color = "blue" if i == max_index else None
            st.write(f"## <span style='color:{color}'>{class_name[i]} : {probli[0][i]*100:.2f}%</span>", unsafe_allow_html=True)

