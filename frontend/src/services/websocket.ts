type MessageListener = (data: any) => void;

class TerminalWebSocketClient {
  private socket: WebSocket | null = null;
  private listeners: Set<MessageListener> = new Set();
  private isConnecting: boolean = false;
  private reconnectTimeout: any = null;
  private url: string;

  constructor() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    this.url = `${protocol}//${host}/ws/terminal`;
  }

  public connect() {
    if (this.socket && (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)) {
      return;
    }

    this.isConnecting = true;
    try {
      this.socket = new WebSocket(this.url);

      this.socket.onopen = () => {
        this.isConnecting = false;
        console.log('[WS] Connected to Kali PTY terminal');
        this.notifyListeners({ type: 'connection_status', connected: true });
      };

      this.socket.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          this.notifyListeners(msg);
        } catch (e) {
          // If raw text
          this.notifyListeners({ type: 'terminal_output', data: event.data });
        }
      };

      this.socket.onclose = () => {
        this.isConnecting = false;
        this.notifyListeners({ type: 'connection_status', connected: false });
        // Attempt reconnect after 2 seconds
        if (!this.reconnectTimeout) {
          this.reconnectTimeout = setTimeout(() => {
            this.reconnectTimeout = null;
            this.connect();
          }, 2000);
        }
      };

      this.socket.onerror = (err) => {
        console.warn('[WS] Error in terminal connection:', err);
      };
    } catch (e) {
      this.isConnecting = false;
      console.warn('[WS] Connection exception:', e);
    }
  }

  public disconnect() {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  public sendInput(data: string) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type: 'input', data }));
    }
  }

  public sendResize(cols: number, rows: number) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type: 'resize', cols, rows }));
    }
  }

  public subscribe(listener: MessageListener) {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notifyListeners(data: any) {
    this.listeners.forEach((listener) => {
      try {
        listener(data);
      } catch (err) {
        console.error('[WS] Error in listener callback:', err);
      }
    });
  }
}

export const wsClient = new TerminalWebSocketClient();
