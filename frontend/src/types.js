/**
 * @typedef {Object} SourceInfo
 * @property {string} source_file
 * @property {number} similarity_score
 * @property {number} [page]
 * @property {string} content
 */

/**
 * @typedef {Object} Question
 * @property {'MCQ' | 'True/False'} type
 * @property {string} question
 * @property {string[]} options
 * @property {string} answer
 * @property {string} explanation
 */

/**
 * @typedef {Object} QuizResponse
 * @property {Question[]} questions
 * @property {SourceInfo[]} sources
 */

/**
 * @typedef {Object} LearningResponse
 * @property {string} content
 * @property {SourceInfo[]} sources
 */

/**
 * @typedef {Object} HealthCheck
 * @property {string} status
 * @property {number} documents_count
 * @property {string[]} available_sources
 */

/**
 * @typedef {Object} UploadResponse
 * @property {boolean} success
 * @property {string} message
 * @property {number} chunks_added
 * @property {number} pages_processed
 */

/**
 * @typedef {Object} QuizRequest
 * @property {'Easy' | 'Medium' | 'Hard'} difficulty
 * @property {number} num_questions
 * @property {number} top_k
 * @property {number} min_score
 * @property {string[]} [source_filter]
 * @property {string} [topic]
 * @property {('MCQ' | 'True/False')[]} question_types
 */

/**
 * @typedef {Object} LearningRequest
 * @property {'Summary' | 'Key Notes'} mode
 * @property {number} top_k
 * @property {string[]} [source_filter]
 * @property {string} [topic]
 */

/**
 * @typedef {Object} QuizState
 * @property {Question[]} questions
 * @property {SourceInfo[]} sources
 * @property {Record<number, string>} userAnswers
 * @property {boolean} isSubmitted
 * @property {number | null} startTime
 * @property {number} score
 * @property {number} total
 */

/**
 * @typedef {Object} HistoryEntry
 * @property {string} date
 * @property {number} score
 * @property {number} total
 * @property {string} document
 * @property {string} difficulty
 */

/**
 * @typedef {Object} AppState
 * @property {string[]} availableSources
 * @property {string[]} selectedSources
 * @property {number} topK
 * @property {number} similarityThreshold
 * @property {number} numQuestions
 * @property {('MCQ' | 'True/False')[]} questionTypes
 * @property {string} topicFocus
 * @property {'Easy' | 'Medium' | 'Hard'} difficulty
 * @property {boolean} examMode
 * @property {boolean} flashcardMode
 * @property {string} learningContent
 * @property {'Summary' | 'Key Notes'} learningMode
 * @property {SourceInfo[]} learningSources
 * @property {QuizState} quiz
 * @property {HistoryEntry[]} history
 * @property {boolean} isLoading
 * @property {'learning' | 'quiz'} activeTab
 */
