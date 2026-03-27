import { describe, it, expect } from 'vitest';
import {
  formatTime,
  formatDate,
  truncateText,
  calculateScorePercentage,
  getScoreColor,
} from '@/utils/helpers';

describe('formatTime', () => {
  it('formats milliseconds to MM:SS', () => {
    expect(formatTime(0)).toBe('0:00');
    expect(formatTime(1000)).toBe('0:01');
    expect(formatTime(60000)).toBe('1:00');
    expect(formatTime(65000)).toBe('1:05');
    expect(formatTime(3723000)).toBe('62:03');
  });

  it('pads seconds correctly', () => {
    expect(formatTime(5000)).toBe('0:05');
    expect(formatTime(30000)).toBe('0:30');
  });
});

describe('formatDate', () => {
  it('formats date string correctly', () => {
    const date = '2024-01-15T10:30:00.000Z';
    const formatted = formatDate(date);
    // US format: Jan 15, 2024
    expect(formatted).toMatch(/Jan 15, 2024/);
  });

  it('handles different timezones', () => {
    const date = '2024-12-25T00:00:00.000Z';
    const formatted = formatDate(date);
    expect(formatted).toMatch(/Dec 25, 2024/);
  });
});

describe('truncateText', () => {
  it('returns full text if shorter than max', () => {
    expect(truncateText('Hello', 10)).toBe('Hello');
  });

  it('truncates text longer than max', () => {
    expect(truncateText('Hello World!', 5)).toBe('Hello...');
  });

  it('truncates at word boundary when possible', () => {
    expect(truncateText('Hello World Test', 11)).toBe('Hello World...');
  });

  it('handles exact length', () => {
    expect(truncateText('Perfect', 7)).toBe('Perfect');
  });
});

describe('calculateScorePercentage', () => {
  it('calculates percentage correctly', () => {
    expect(calculateScorePercentage(9, 10)).toBe(90);
    expect(calculateScorePercentage(8, 10)).toBe(80);
    expect(calculateScorePercentage(7, 10)).toBe(70);
    expect(calculateScorePercentage(6, 10)).toBe(60);
    expect(calculateScorePercentage(4, 10)).toBe(40);
  });

  it('handles edge cases', () => {
    expect(calculateScorePercentage(0, 10)).toBe(0);
    expect(calculateScorePercentage(10, 10)).toBe(100);
  });

  it('rounds percentage correctly', () => {
    expect(calculateScorePercentage(7, 9)).toBe(78); // 77.78% → 78%
  });
});

describe('getScoreColor', () => {
  it('returns green for high scores', () => {
    expect(getScoreColor(70)).toBe('text-green-400');
    expect(getScoreColor(100)).toBe('text-green-400');
  });

  it('returns yellow for medium scores', () => {
    expect(getScoreColor(50)).toBe('text-yellow-400');
    expect(getScoreColor(69)).toBe('text-yellow-400');
  });

  it('returns red for low scores', () => {
    expect(getScoreColor(49)).toBe('text-red-400');
    expect(getScoreColor(0)).toBe('text-red-400');
  });
});

describe('cn (classnames utility)', () => {
  it('joins truthy class strings', () => {
    expect(cn('a', 'b', 'c')).toBe('a b c');
  });

  it('filters out falsy values', () => {
    expect(cn('a', false, null, undefined, 'b')).toBe('a b');
  });

  it('handles empty input', () => {
    expect(cn()).toBe('');
    expect(cn(false, null, undefined)).toBe('');
  });

  it('handles mix of strings and conditions', () => {
    const condition = true;
    const condition2 = false;
    expect(cn('base', condition && 'conditional', condition2 && 'skipped')).toBe('base conditional');
  });
});
