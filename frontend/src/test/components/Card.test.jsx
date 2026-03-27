import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';

describe('Card', () => {
  it('renders children correctly', () => {
    render(<Card>Card content</Card>);
    expect(screen.getByText('Card content')).toBeInTheDocument();
  });

  it('applies glassmorphism classes', () => {
    render(<Card>Test</Card>);
    const card = screen.getByText('Test').parentElement;
    expect(card).toHaveClass('bg-card-bg', 'backdrop-blur-glass', 'border-glass-border');
  });

  it('applies hover classes when hover prop is true', () => {
    render(<Card hover>Hover card</Card>);
    const card = screen.getByText('Hover card').parentElement;
    expect(card).toHaveClass('hover:border-primary-500');
  });

  it('applies padding classes correctly', () => {
    const { rerender } = render(<Card padding="sm">Small padding</Card>);
    expect(screen.getByText('Small padding').parentElement).toHaveClass('p-4');

    rerender(<Card padding="lg">Large padding</Card>);
    expect(screen.getByText('Large padding').parentElement).toHaveClass('p-8');
  });

  it('passes custom className', () => {
    render(<Card className="custom-class">Test</Card>);
    const card = screen.getByText('Test').parentElement;
    expect(card).toHaveClass('custom-class');
  });
});

describe('CardHeader', () => {
  it('renders children', () => {
    render(<CardHeader>Header content</CardHeader>);
    expect(screen.getByText('Header content')).toBeInTheDocument();
  });

  it('applies margin bottom', () => {
    render(<CardHeader>Header</CardHeader>);
    expect(screen.getByText('Header').parentElement).toHaveClass('mb-4');
  });
});

describe('CardTitle', () => {
  it('renders text', () => {
    render(<CardTitle>Title</CardTitle>);
    expect(screen.getByText('Title')).toBeInTheDocument();
  });

  it('applies heading styles', () => {
    render(<CardTitle>Title</CardTitle>);
    expect(screen.getByRole('heading', { level: 3 })).toHaveClass(
      'text-xl',
      'font-bold',
      'text-dark-100'
    );
  });
});

describe('CardContent', () => {
  it('renders children', () => {
    render(<CardContent>Content area</CardContent>);
    expect(screen.getByText('Content area')).toBeInTheDocument();
  });
});
