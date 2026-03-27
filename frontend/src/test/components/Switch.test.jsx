import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Switch } from '@/components/ui/Switch';

describe('Switch', () => {
  it('renders unchecked by default', () => {
    render(<Switch checked={false} onChange={() => {}} />);
    const checkbox = screen.getByRole('checkbox');
    expect(checkbox).not.toBeChecked();
  });

  it('renders checked when checked prop is true', () => {
    render(<Switch checked={true} onChange={() => {}} />);
    const checkbox = screen.getByRole('checkbox');
    expect(checkbox).toBeChecked();
  });

  it('calls onChange when clicked', () => {
    const handleChange = vi.fn();
    render(<Switch checked={false} onChange={handleChange} />);

    fireEvent.click(screen.getByRole('checkbox'));
    expect(handleChange).toHaveBeenCalledWith(true);
  });

  it('renders label when provided', () => {
    render(<Switch checked={false} onChange={() => {}} label="Enable feature" />);
    expect(screen.getByText('Enable feature')).toBeInTheDocument();
  });

  it('is disabled when disabled prop is true', () => {
    render(<Switch checked={false} onChange={() => {}} disabled />);
    expect(screen.getByRole('checkbox')).toBeDisabled();
  });

  it('has correct visual styling for checked state', () => {
    const { rerender } = render(<Switch checked={false} onChange={() => {}} />);
    const track = screen.getByRole('checkbox').parentElement;
    expect(track).toHaveClass('bg-dark-600');

    rerender(<Switch checked={true} onChange={() => {}} />);
    expect(track).toHaveClass('bg-primary-600');
  });

  it('dot translates when checked', () => {
    const { rerender } = render(<Switch checked={false} onChange={() => {}} />);
    const dot = document.querySelector('.dot')!;
    expect(dot).toHaveClass('translate-x-0');

    rerender(<Switch checked={true} onChange={() => {}} />);
    expect(dot).toHaveClass('translate-x-4');
  });
});
