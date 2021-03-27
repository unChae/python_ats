#status(int) : 200성공 404찾을수 없음 400에러
#msg(string) : 메세지 전송
#data([{"key":"value"}]) : key:value
def cus_respones(status, msg, data):
    
    return {
        "status": status,
        "msg": msg,
        "data": data
    }