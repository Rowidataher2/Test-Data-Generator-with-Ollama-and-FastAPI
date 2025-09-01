"use client";

import { useState } from "react";

export default function Home() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const userId = 1; // mock user ID

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8001/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
          user_request: input,
          messages: newMessages,
        }),
      });

      const data = await res.json();
      if (res.ok) {
        setMessages(data.messages);
      } else {
        setErrorMsg(data.detail || "Error communicating with model.");
      }
    } catch (err) {
      console.error("Chat error:", err);
      setErrorMsg("Error connecting to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-xl font-bold mb-4">Test Data Generator Chat</h1>

      <div className="border rounded p-4 h-96 overflow-y-auto bg-gray-50">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`mb-2 p-2 rounded ${
              msg.role === "user"
                ? "bg-blue-100 text-right"
                : "bg-green-100 text-left"
            }`}
          >
            <p className="whitespace-pre-wrap">
              {typeof msg.content === "string"
                ? msg.content
                : JSON.stringify(msg.content, null, 2)}
            </p>
          </div>
        ))}
      </div>

      <form onSubmit={handleSend} className="mt-4 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 border p-2 rounded"
          placeholder="Type your schema request..."
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded"
          disabled={loading}
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </form>

      {errorMsg && <p className="text-red-500 mt-2">{errorMsg}</p>}
    </div>
  );
}
