(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (handempty)
    (clear a)
    (ontable c)
    (on e c)
    (on f e)
    (on b f)
    (on d b)
    (on a d)
  )
  (:goal (and
    (on e f)
    (on f a)
    (on a b)
    (on b c)
    (on c d)
  ))
)
