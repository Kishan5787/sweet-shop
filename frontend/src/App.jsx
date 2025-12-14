import { useEffect, useState } from "react";
import { getAllSweets, purchaseSweet } from "./api";

function App() {
  const [sweets, setSweets] = useState([]);
  const [error, setError] = useState("");

  const loadSweets = () => {
    getAllSweets()
      .then(setSweets)
      .catch((err) => setError(err.message));
  };

  useEffect(() => {
    loadSweets();
  }, []);

  const handlePurchase = async (id) => {
    try {
      await purchaseSweet(id);
      loadSweets(); // refresh quantity
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>🍬 Sweet Shop</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {Array.isArray(sweets) &&
        sweets.map((s) => (
          <div
            key={s.id}
            style={{
              border: "1px solid #ccc",
              margin: 10,
              padding: 10,
              width: 250,
            }}
          >
            <h3>{s.name}</h3>
            <p>Category: {s.category}</p>
            <p>Price: ₹{s.price}</p>
            <p>Quantity: {s.quantity}</p>

            <button
              onClick={() => handlePurchase(s.id)}
              disabled={s.quantity <= 0}
            >
              Purchase
            </button>
          </div>
        ))}
    </div>
  );
}

export default App;
