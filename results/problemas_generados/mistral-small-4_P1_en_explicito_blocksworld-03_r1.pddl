(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear a)
    (handempty)
    (on a d)
    (on b f)
    (on c table)
    (on d b)
    (on e c)
    (on f e)
  )
  (:goal (and
    (on a b)
    (on b c)
    (on c d)
    (on e f)
    (on f a)
  ))
)
