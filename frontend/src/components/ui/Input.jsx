import React from 'react';
import clsx from 'clsx';

export const Input = ({
  label,
  error,
  helperText,
  className,
  ...props
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-dark-200 mb-2">
          {label}
        </label>
      )}
      <input
        className={clsx(
          'w-full px-4 py-2 bg-dark-800 border rounded-lg text-dark-100 placeholder-dark-400 focus:outline-none focus:ring-2 transition-colors',
          error
            ? 'border-red-500 focus:ring-red-500'
            : 'border-dark-600 focus:ring-primary-500 focus:border-transparent',
          className
        )}
        {...props}
      />
      {error && <p className="mt-1 text-sm text-red-400">{error}</p>}
      {helperText && !error && (
        <p className="mt-1 text-sm text-dark-400">{helperText}</p>
      )}
    </div>
  );
};

export const Textarea = ({
  label,
  error,
  helperText,
  className,
  ...props
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-dark-200 mb-2">
          {label}
        </label>
      )}
      <textarea
        className={clsx(
          'w-full px-4 py-2 bg-dark-800 border rounded-lg text-dark-100 placeholder-dark-400 focus:outline-none focus:ring-2 resize-y min-h-[100px]',
          error
            ? 'border-red-500 focus:ring-red-500'
            : 'border-dark-600 focus:ring-primary-500 focus:border-transparent',
          className
        )}
        {...props}
      />
      {error && <p className="mt-1 text-sm text-red-400">{error}</p>}
      {helperText && !error && (
        <p className="mt-1 text-sm text-dark-400">{helperText}</p>
      )}
    </div>
  );
};

export const Select = ({
  label,
  error,
  options,
  className,
  ...props
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-dark-200 mb-2">
          {label}
        </label>
      )}
      <select
        className={clsx(
          'w-full px-4 py-2 bg-dark-800 border rounded-lg text-dark-100 focus:outline-none focus:ring-2 cursor-pointer',
          error
            ? 'border-red-500 focus:ring-red-500'
            : 'border-dark-600 focus:ring-primary-500 focus:border-transparent',
          className
        )}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <p className="mt-1 text-sm text-red-400">{error}</p>}
    </div>
  );
};
