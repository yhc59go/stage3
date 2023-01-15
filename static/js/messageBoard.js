const inputFile=document.getElementById("inputFile");
var imagefromUser;

window.addEventListener("load", function(event) {
    getContentOfMessageBoard();
    
});

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
                            fetch("/api/messageBoard/content", 
                                    {
                                        method: "POST",
                                        body: formData
                                    }
                                );        
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
            for(let i=0;i<data.data.length;i++){
                const messageBoardArea=document.getElementById("messageBoardArea");
                const messageContent=document.createElement("div");
                messageContent.classList.add('messageContent');

                //text from User 
                const textContentFromUser=document.createElement("div");
                textContentFromUser.classList.add('textContent');
                textContentFromUser.textContent=data.data[i][0];

                //image from User
                const imgContent=document.createElement("div");
                imgContent.classList.add('imgContent');
                imgContent.style.backgroundImage = "url('" + data.data[i][1] + "')";
                
                var imgGetSize = new Image();
                imgGetSize.src = data.data[i][1];
                imgGetSize.onload = function() {
                    imgContent.style.width=(imgGetSize.width/2)+"px";
                    imgContent.style.height=(imgGetSize.height/2)+"px";
                };
                messageContent.appendChild(textContentFromUser);
                messageContent.appendChild(imgContent);
                messageBoardArea.appendChild(messageContent);
            }
        }
    ).catch((err) => alert(err));
}


