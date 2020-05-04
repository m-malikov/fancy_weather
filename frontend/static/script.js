function create_message(from_user) {
    let message = document.createElement("div")
    message.classList.add("message")
    message.classList.add(from_user ? "user_message" : "bot_message")
    return message
}

function add_text(message, text) {
    let message_box = document.createElement("div")
    message_box.classList.add("message_box")
    message_box.innerHTML = text.split("\n").join("<br>\n")
    
    message.appendChild(message_box)
    return message
}

function add_image(message, url) {
    let image_box = document.createElement("div")
    image_box.classList.add("image_box")
    
    let image = document.createElement("img")
    image.src = url
    
    image_box.appendChild(image)
    message.appendChild(image_box)
    return message
}

function insert_message(message) {
    let chat_box = document.getElementById("chat_box")
    chat_box.appendChild(message)
}

function add_user_message(text) {
    let m = create_message(true)
    m = add_text(m, text)
    insert_message(m)
}

function add_bot_message(text, image) {
    let m = create_message(false)
    m = add_text(m, text)
    insert_message(m)
    
    if (image) {
        let m = create_message(false)
        m = add_image(m, image)
        insert_message(m)
    }
}

function show_error(error) {
    console.error(error)
    add_bot_message("Произошла ошибка", null)
}

function send_request(text) {
    text = text.trim()
    if (text === "") {
        return
    }
    add_user_message(text)
    
    fetch("/api/v1/weather?text=" + encodeURI(text))
        .then(response => {
            if (!response.ok) {
                show_error(response.text())
            } else {
                json = response.json()
                    .then(json => add_bot_message(json.text, json.picture))
                    .catch(error => show_error(error))
            }
        })
        .catch(error => show_error(error))
}

let question_field = document.getElementById("question_field")
question_field.addEventListener("keyup", event => {
    if (event.which === 13 || event.keyCode === 13) {
        let text = question_field.value
        question_field.value = ""
        send_request(text)
    }
})

send_request("Какая погода  сегодня?")

