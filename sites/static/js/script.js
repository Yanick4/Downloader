function download(){
    const form=document.querySelector('form')
    form.addEventListener("submit",_=>{
        _.preventDefault()
        const formData=new FormData(form)
        const data=Object.fromEntries(formData)
        const csrf_token=data.csrfmiddlewaretoken
        fetch('download-api',{
            method:"POST",
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body:JSON.stringify(data)
        }).then(response=>response.json()).then(data=>{
            
        })
    })
}



function show_video_in_iframe(){
    const extractYouTubeVideoId=(url) =>{
        const patterns = [
            /(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)/,  // format www.youtube.com/watch?v=VIDEO_ID
            /(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)/,  // format youtu.be/VIDEO_ID
            /(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]+)/  // format youtube.com/v/VIDEO_ID
        ];
        
        for (let pattern of patterns) {
            const match = url.match(pattern);
            if (match) {
                return match[1];  // Retourne l'ID de la vidéo
            }
        }
        return null;
    }

    // Exemple d'utilisation
    const frame=document.querySelector("iframe")
    const input=document.querySelector('.input input')
    const title=document.querySelector(".title")
    input.addEventListener("change",e=>{
        const {value}=e.target
        const videoId = extractYouTubeVideoId(value);
        frame.src=``
        frame.src=`https://www.youtube.com/embed/${videoId}`
        // Extract meta data
        fetch(`video-meta-data?url=${value}`).then(response=>response.json()).then(data=>{
            if (title){
                title.innerHTML=`${data}`
            }
        })
    })
}




window.addEventListener("DOMContentLoaded",_=>{
    download()
    show_video_in_iframe()
})