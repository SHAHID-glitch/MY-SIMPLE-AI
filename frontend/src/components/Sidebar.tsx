import React, { useState } from 'react';
import { useChat } from '../hooks/useChat';
import { Plus, Trash2, ChevronDown } from 'lucide-react';

export const Sidebar: React.FC = () => {
  const { conversations, currentConversation, createNewConversation, loadConversation, deleteConversation } = useChat();
  const [expanded, setExpanded] = useState(true);

  const handleDelete = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (window.confirm('Delete this conversation?')) {
      deleteConversation(id);
    }
  };

  return (
    <div className={`bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col transition-all ${expanded ? 'w-64' : 'w-20'}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        {expanded && <h2 className="font-bold text-gray-900 dark:text-white">Chats</h2>}
        <button
          onClick={() => setExpanded(!expanded)}
          className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
        >
          <ChevronDown size={20} className={`transition-transform ${expanded ? '' : 'rotate-90'}`} />
        </button>
      </div>

      {/* New Chat Button */}
      <button
        onClick={createNewConversation}
        className="m-2 p-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg flex items-center justify-center gap-2 font-medium transition-colors"
      >
        <Plus size={20} />
        {expanded && 'New Chat'}
      </button>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto">
        {conversations.length === 0 ? (
          expanded && (
            <p className="p-4 text-sm text-gray-500 dark:text-gray-400">No conversations yet</p>
          )
        ) : (
          conversations.map(conv => (
            <button
              key={conv.id}
              onClick={() => loadConversation(conv.id)}
              className={`w-full text-left p-3 m-2 rounded-lg transition-colors group flex items-start justify-between ${
                currentConversation?.id === conv.id
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100'
                  : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-900 dark:text-gray-100'
              }`}
            >
              {expanded && (
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate text-sm">{conv.title}</p>
                  <p className="text-xs opacity-70 mt-1">{conv.messages.length} messages</p>
                </div>
              )}
              <div
                onClick={(e) => handleDelete(e, conv.id)}
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-100 dark:hover:bg-red-900 rounded transition-opacity flex-shrink-0 cursor-pointer"
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    handleDelete(e as any, conv.id);
                  }
                }}
              >
                <Trash2 size={16} className="text-red-600 dark:text-red-400" />
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  );
};
