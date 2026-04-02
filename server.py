import socket
import threading
import time

# 항상 1P와 2P의 좌표만 관리
players = {
    1: {"x": -100.0, "y": -100.0},
    2: {"x": -100.0, "y": -100.0}
}
clients = []

def handle_client(conn, p_id):
    global players
    # ⭐️ 3, 4, 5번째 접속해도 홀수면 1P, 짝수면 2P로 강제 역할 부여!
    my_role = 1 if p_id % 2 != 0 else 2 
    
    try:
        conn.sendall(f"{my_role}\n".encode('utf-8'))
        time.sleep(0.1)

        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data: break

            messages = data.strip().split('\n')
            if messages and messages[-1]:
                try:
                    x_str, y_str = messages[-1].split(',')
                    players[my_role]["x"] = float(x_str)
                    players[my_role]["y"] = float(y_str)
                except:
                    pass

            # 두 플레이어의 좌표를 중계
            state_msg = f"{players[1]['x']},{players[1]['y']}|{players[2]['x']},{players[2]['y']}\n"
            conn.sendall(state_msg.encode('utf-8'))

    except Exception as e:
        pass

    print(f"[알림] 접속 종료 (역할: {my_role}P)")
    if conn in clients:
        clients.remove(conn)
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("=== 🎮 3D 게임 멀티플레이 서버 오픈 (포트 5555) ===")

    connection_count = 1
    while True:
        conn, addr = server.accept()
        print(f"[알림] 새로운 접속자: {addr}")
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, connection_count), daemon=True).start()
        connection_count += 1

if __name__ == "__main__":
    start_server()
