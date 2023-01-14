const inputFile=document.getElementById("inputFile");
var imagefromUser;
inputFile.addEventListener("change", function() {
                                        var file = inputFile.files[0];
                                        var reader = new FileReader();
                                        reader.onload = function() {
                                            //將圖片轉為二進位流格式
                                            const imageAsBinary = reader.result;
                                            //將圖片轉為Blob物件
                                            var blob = new Blob([imageAsBinary], { type: 'image/jpeg' });
                                            imagefromUser = blob;
                                        };
                                        reader.readAsArrayBuffer(file);
                                    }
);

const submitButton = document.getElementById('submitButton');
submitButton.addEventListener("click",
                        function(){
                            //get text content from user
                            let textContentFromUser=document.getElementById("textContentFromUser");  
                            //send data to back-end   
                            let formData = new FormData();
                            formData.append('text', textContentFromUser.value);
                            formData.append('image', imagefromUser);
                            fetch("/api/user/image", 
                                    {
                                        method: "POST",
                                        body: formData
                                    }
                                );        
                        }
);



