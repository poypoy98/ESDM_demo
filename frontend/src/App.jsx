import { useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendQuery = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setMessages((msgs) => [...msgs, { sender: "user", text: query }]);

    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session: "demo", query }),
    });
    const data = await res.json();

    const botMessage = {
      sender: "bot",
      text: `**SPARQL Query:**\n${data.sparql}\n\n**Results:**\n${JSON.stringify(
        data.results,
        null,
        2
      )}`,
    };
    setMessages((msgs) => [...msgs, botMessage]);
    setQuery("");
    setLoading(false);
  };

  return (
    <div className="h-screen flex flex-col p-4 bg-gray-50">
      <h1 className="text-2xl font-bold mb-4 text-center">ESDM Semantic Chat</h1>
      <div className="flex-1 overflow-y-auto p-4 bg-white rounded-xl shadow-inner">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`mb-2 p-2 rounded-xl ${
              m.sender === "user" ? "bg-blue-100 text-right" : "bg-green-100"
            }`}
          >
            <pre className="whitespace-pre-wrap">{m.text}</pre>
          </div>
        ))}
        {loading && <div className="italic text-gray-500">Thinking...</div>}
      </div>
      <div className="flex mt-4">
        <input
          className="flex-1 border p-2 rounded-xl"
          placeholder="Ask something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendQuery()}
        />
        <button
          onClick={sendQuery}
          className="ml-2 bg-blue-600 text-white px-4 py-2 rounded-xl"
        >
          Send
        </button>
      </div>
    </div>
  );
}
