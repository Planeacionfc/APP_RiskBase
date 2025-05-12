import { useEffect, useState } from 'react';
import { jwtDecode } from 'jwt-decode';

interface JwtPayload {
  role?: string;
  [key: string]: any;
}

export function useAuth() {
  const [role, setRole] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    if (token) {
      try {
        const decoded = jwtDecode<JwtPayload>(token);
        setRole(decoded.role ?? null);
      } catch {
        setRole(null);
      }
    } else {
      setRole(null);
    }
    setLoading(false);
  }, []);

  return { role, loading };
}
