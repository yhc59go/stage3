const inputFile=document.getElementById("inputFile");
var imagefromUser="";

window.addEventListener("load", function(event) {
    getContentOfMessageBoard();  
});

inputFile.addEventListener("change", function() {
                                        let file = inputFile.files[0];
                                        if(file){
                                            var reader = new FileReader();
                                            reader.onload = function() {
                                                //將圖片轉為二進位流格式
                                                const imageAsBinary = reader.result;
                                                //將圖片轉為Blob物件
                                                var blob = new Blob([imageAsBinary], { type: 'image/jpeg' });
                                                imagefromUser = blob;
                                            };
                                            reader.readAsArrayBuffer(file);
                                        }else{
                                            imagefromUser="";
                                        }
                                        
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
                            if(!imagefromUser){
                                //No image from user 
                                imagefromUser="";
                            }
                            formData.append('image', imagefromUser);
                            
                            fetch("/api/messageBoard/content", 
                                    {
                                        method: "POST",
                                        body: formData
                                    }
                                ).then(response => response.json())
                            .then(function(data){
                                    if(data.ok==true){
                                        getContentLastOneOfMessageBoard();
                                    }else if(data.error==true){
                                        alert(data.message);
                                    }   
                                }
                            ).catch(error => (console.log(error)));
                        }
);

function getContentOfMessageBoard(){
    src="/api/messageBoard/content"
    fetch(src,
        {
            method: "GET",
            headers: {
                'accept': 'application/json'
            }
        }
    ).then(function(response){
            return response.json();
        }
    ).then(function(data){
        if(data.data){

            for(let i=0;i<data.data.length;i++){
                const messageContainer=document.getElementById("messageContainer");
                const messageContent=document.createElement("div");
                messageContent.classList.add('messageContent');

                //text from User 
                const textContentFromUser=document.createElement("div");
                textContentFromUser.classList.add('textContent');
                textContentFromUser.textContent=data.data[i][1];

                //image from User
                const imgContent=document.createElement("div");
                imgContent.classList.add('imgContent');
                imgContent.style.backgroundImage = "url('" + data.data[i][2] + "')";
                if(data.data[i][2]){
                    var imgGetSize = new Image();
                    imgGetSize.src = data.data[i][2];
                    imgGetSize.onload = function() {
                        imgContent.style.width=(imgGetSize.width/2)+"px";
                        imgContent.style.height=(imgGetSize.height/2)+"px";
                    };
                }

                messageContent.appendChild(textContentFromUser);
                messageContent.appendChild(imgContent);

                if(messageContainer.firstElementChild){
                    messageContainer.insertBefore(messageContent, messageContainer.firstElementChild);
                }else{
                    messageContainer.appendChild(messageContent);
                }
                
            }
        }else if(data.error==true){
            alert(data.message);
        }
            
    }).catch((err) => alert(err));
}


function getContentLastOneOfMessageBoard(){
    src="/api/messageBoard/content"
    fetch(src,
        {
            method: "GET",
            headers: {
                'accept': 'application/json'
            }
        }
    ).then(function(response){
            return response.json();
        }
    ).then(function(data){
        if(data.data){
            
            let idxOfLastData=data.data.length-1;
            
            const messageContainer=document.getElementById("messageContainer");

            const messageContent=document.createElement("div");
            messageContent.classList.add('messageContent');

            //text from User 
            const textContentFromUser=document.createElement("div");
            textContentFromUser.classList.add('textContent');
            textContentFromUser.textContent=data.data[idxOfLastData][1];

            //image from User
            const imgContent=document.createElement("div");
            imgContent.classList.add('imgContent');
            imgContent.style.backgroundImage = "url('" + data.data[idxOfLastData][2] + "')";
            
            if(data.data[idxOfLastData][2]){
                let imgGetSize = new Image();
                imgGetSize.src = data.data[idxOfLastData][2];
                imgGetSize.onload = function() {
                    imgContent.style.width=(imgGetSize.width/2)+"px";
                    imgContent.style.height=(imgGetSize.height/2)+"px";
                };
            }
            
            messageContent.appendChild(textContentFromUser);
            messageContent.appendChild(imgContent);

            if(messageContainer.firstElementChild){
                messageContainer.insertBefore(messageContent, messageContainer.firstElementChild);
            }else{
                messageContainer.appendChild(messageContent);
            }
        }else if(data.error){
            alert(data.message);
        }
            
    }).catch((err) => alert(err));
}
