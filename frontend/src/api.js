const BASE_URL = "https://sweet-shop-kcz9.onrender.com";

// 🔑 TOKEN (temporary hardcoded)
const TOKEN =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbmlrZXQyIiwiZXhwIjoxNzY1ODEwODc3fQ.lsMUJsHXmdAKLNEGZzHaKVuQ5ZIe7KqTnBt2IUQds9s";

export async function getAllSweets() {
  const res = await fetch(`${BASE_URL}/api/sweets`, {
    headers: {
      Authorization: `Bearer ${TOKEN}`,
    },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch sweets");
  }

  return res.json();
}

export async function purchaseSweet(id) {
  const res = await fetch(`${BASE_URL}/api/sweets/${id}/purchase`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${TOKEN}`,
    },
  });

  if (!res.ok) {
    throw new Error("Purchase failed");
  }

  return res.json();
}
