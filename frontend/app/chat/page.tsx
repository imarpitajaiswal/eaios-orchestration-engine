"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { fetchWithAuth } from "../../lib/api";

interface Message {
  role: "user" | "agent" | "system";
  content: string;
}

export default function ChatDashboard() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  // 1. Client-Side Route Protection
  useEffect(() => {
    const token = localStorage.getItem("eaios_access_token");
    if (!token) {
      router.push("/login"); // Kick unauthorized users back to the gateway
    }
  }, [router]);

  // 2. The Agent Execution Trigger
  const handleInvokeAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const currentMessage = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: currentMessage }]);
    setIsLoading(true);

    try {
      // Securely route the prompt through our FastAPI orchestration layer
      const data = await fetchWithAuth("/chat/invoke", {
        method: "POST",
        body: JSON.stringify({ message: currentMessage }),
      });

      setMessages((prev) => [...prev, { role: "agent", content: data.response }]);
    } catch (error: any) {
      setMessages((prev) => [
        ...prev,
        { role: "system", content: `Execution Error: ${error.message}` },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // 3. Enterprise UI Render
  return (
    <div className="flex flex-col h-screen bg-gray-50 text-black">
      <header className="bg-slate-900 text-white p-4 shadow-md flex justify-between items-center">
        <h1 className="text-xl font-bold tracking-tight">EAIOS Intelligence Core</h1>
        <button 
          onClick={() => {
            localStorage.removeItem("eaios_access_token");
            router.push("/login");
          }}
          className="text-sm bg-slate-800 hover:bg-slate-700 px-3 py-1 rounded border border-slate-600"
        >
          Terminate Session
        </button>
      </header>

      <main className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-400 mt-20">
            System Online. Awaiting executive input...
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-lg max-w-3xl ${
                msg.role === "user"
                  ? "bg-blue-100 text-blue-900 ml-auto border border-blue-200"
                  : msg.role === "system"
                  ? "bg-red-100 text-red-900 border border-red-200"
                  : "bg-white text-gray-900 border border-gray-200 shadow-sm"
              }`}
            >
              <span className="text-xs font-bold uppercase tracking-wider opacity-50 block mb-1">
                {msg.role}
              </span>
              {msg.content}
            </div>
          ))
        )}
        {isLoading && (
          <div className="bg-white p-4 rounded-lg max-w-3xl border border-gray-200 shadow-sm animate-pulse text-gray-500">
            Agent reasoning cycle active...
          </div>
        )}
      </main>

      <footer className="p-4 bg-white border-t border-gray-200">
        <form onSubmit={handleInvokeAgent} className="max-w-4xl mx-auto flex gap-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Issue a command to the orchestration engine..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading}
            className="px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none disabled:opacity-50 transition-colors"
          >
            Execute
          </button>
        </form>
      </footer>
    </div>
  );
}