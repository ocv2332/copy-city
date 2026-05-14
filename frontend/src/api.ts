import type {
  ApiValidationError,
  CartItem,
  CreateProductPayload,
  Order,
  OrderStatus,
  Product,
  RegisterPayload,
  TokenResponse,
  User,
  UserRole,
} from './types';

const AUTH_API_URL = import.meta.env.VITE_AUTH_API_URL || 'http://localhost:8000/api/v1';
const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL || 'http://localhost:8001/api/v1';

const TOKEN_KEY = 'copy_city_access_token';

export const authStore = {
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  },
  setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token);
  },
  clear(): void {
    localStorage.removeItem(TOKEN_KEY);
  },
};

async function parseResponse<T>(response: Response): Promise<T> {
  if (response.status === 204) {
    return null as T;
  }

  const contentType = response.headers.get('content-type') || '';
  const payload: unknown = contentType.includes('application/json')
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const detail = typeof payload === 'object' && payload !== null && 'detail' in payload
      ? (payload as { detail?: string | ApiValidationError[] }).detail
      : payload;
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg).filter(Boolean).join(', ')
      : String(detail || 'Ошибка запроса');
    throw new Error(message);
  }

  return payload as T;
}

async function request<T>(url: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  const token = authStore.getToken();

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include',
  });

  return parseResponse<T>(response);
}

export const authApi = {
  async login(email: string, password: string): Promise<TokenResponse> {
    const body = new URLSearchParams();
    body.set('username', email);
    body.set('password', password);

    const result = await request<TokenResponse>(`${AUTH_API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body,
    });

    authStore.setToken(result.access_token);
    return result;
  },

  register(payload: RegisterPayload): Promise<User> {
    return request<User>(`${AUTH_API_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
  },

  check(): Promise<User> {
    return request<User>(`${AUTH_API_URL}/check`);
  },

  async refresh(): Promise<TokenResponse> {
    const result = await request<TokenResponse>(`${AUTH_API_URL}/refresh`, {
      method: 'POST',
    });
    authStore.setToken(result.access_token);
    return result;
  },

  async logout(): Promise<void> {
    try {
      await request<void>(`${AUTH_API_URL}/logout`, {
        method: 'POST',
      });
    } finally {
      authStore.clear();
    }
  },

  updateUserRole(userId: string, role: UserRole): Promise<User> {
    return request<User>(`${AUTH_API_URL}/users/${userId}/role`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ role }),
    });
  },
};

export const backendApi = {
  getProducts(): Promise<Product[]> {
    return request<Product[]>(`${BACKEND_API_URL}/products`);
  },

  createProduct(payload: CreateProductPayload): Promise<Product> {
    return request<Product>(`${BACKEND_API_URL}/products`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
  },

  uploadPhoto(productId: string, file: File) {
    const body = new FormData();
    body.append('file', file);

    return request(`${BACKEND_API_URL}/products/${productId}/photos`, {
      method: 'POST',
      body,
    });
  },

  getPhotoUrl(photoId: string): string {
    return `${BACKEND_API_URL}/photos/${photoId}`;
  },

  getOrders(): Promise<Order[]> {
    return request<Order[]>(`${BACKEND_API_URL}/orders`);
  },

  async createOrder(items: CartItem[], comment: string): Promise<Order> {
    const total = items.reduce((sum, item) => sum + Number(item.base_price) * item.quantity, 0);
    const order = await request<Order>(`${BACKEND_API_URL}/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        total_amount: total,
        comment: comment || null,
      }),
    });

    for (const item of items) {
      await request(`${BACKEND_API_URL}/orders/${order.id}/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          product_id: item.id,
          quantity: item.quantity,
        }),
      });
    }

    return request<Order>(`${BACKEND_API_URL}/orders/${order.id}`);
  },

  updateOrderStatus(orderId: string, status: OrderStatus): Promise<Order> {
    const params = new URLSearchParams({ status_value: status });
    return request<Order>(`${BACKEND_API_URL}/orders/${orderId}/status?${params.toString()}`, {
      method: 'PATCH',
    });
  },
};
