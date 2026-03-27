import React from 'react';
import clsx from 'clsx';
import { AlertCircle, CheckCircle, Info, XCircle } from 'lucide-react';

export const Alert = ({
  children,
  variant = 'info',
  className,
  dismissible = false,
  onDismiss,
}) => {
  const variants = {
    info: {
      container: 'bg-blue-500/10 border-blue-500/30 text-blue-200',
      icon: <Info className="w-5 h-5 text-blue-400" />,
    },
    success: {
      container: 'bg-green-500/10 border-green-500/30 text-green-200',
      icon: <CheckCircle className="w-5 h-5 text-green-400" />,
    },
    warning: {
      container: 'bg-yellow-500/10 border-yellow-500/30 text-yellow-200',
      icon: <AlertCircle className="w-5 h-5 text-yellow-400" />,
    },
    error: {
      container: 'bg-red-500/10 border-red-500/30 text-red-200',
      icon: <XCircle className="w-5 h-5 text-red-400" />,
    },
  };

  return (
    <div
      className={clsx(
        'relative flex items-start p-4 rounded-xl border',
        variants[variant].container,
        className
      )}
      role="alert"
    >
      <div className="flex-shrink-0 mr-3">{variants[variant].icon}</div>
      <div className="flex-1">{children}</div>
      {dismissible && onDismiss && (
        <button
          type="button"
          onClick={onDismiss}
          className="ml-4 text-current opacity-70 hover:opacity-100"
        >
          <XCircle className="w-5 h-5" />
        </button>
      )}
    </div>
  );
};
