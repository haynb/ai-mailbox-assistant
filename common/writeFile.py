import threading


def write_email_to_file(subject, sender, date, summary, file_path):
    """
    将邮件信息写入到文件中。如果文件不存在，则创建新文件；如果文件已存在，则在文件末尾追加内容。

    :param subject: 邮件主题
    :param sender: 发件人
    :param date: 发送日期
    :param summary: 内容概要
    :param file_path: 文件路径
    """
    # 使用锁来处理并发写入的问题
    lock = threading.Lock()
    with lock:
        # 使用'a'模式打开文件，如果文件不存在则创建文件
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"主题: {subject}\n")
            file.write(f"发件人: {sender}\n")
            file.write(f"日期: {date}\n")
            file.write(f"概要: {summary}\n")
            file.write("=============================================\n")
            file.write("\n\n")