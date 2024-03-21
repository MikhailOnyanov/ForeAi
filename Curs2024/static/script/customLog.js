const messages_levels = {0: 'Info:', 1: 'Warning:', 2: 'Critical:'};
export var counter = 1;
export function writeMsg(msg, lvl) {
        let ms_field = document.querySelector('#sys-msgs');
        let node = document.createElement('li');
        node.appendChild(document.createTextNode(
            messages_levels[lvl] + `[${counter}]:` + " " + msg)
        );
        // добавляем сообщение
        ms_field.appendChild(node);
        counter += 1;
        // скроллим до самого низа
        document.querySelector('.system-messages').scrollTop = document.querySelector('.system-messages').scrollHeight;
    }