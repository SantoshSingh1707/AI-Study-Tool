import React from 'react';

export const Switch = ({
  checked,
  onChange,
  label,
  disabled = false,
}) => {
  return (
    <label
      className={`inline-flex items-center cursor-pointer ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      <div className="relative">
        <input
          type="checkbox"
          className="sr-only"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
          disabled={disabled}
        />
        <div
          className={`block w-10 h-6 rounded-full transition-colors ${
            checked ? 'bg-primary-600' : 'bg-dark-600'
          }`}
        ></div>
        <div
          className={`dot absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform ${
            checked ? 'translate-x-4' : 'translate-x-0'
          }`}
        ></div>
      </div>
      {label && <span className="ml-3 text-sm text-dark-200">{label}</span>}
    </label>
  );
};
