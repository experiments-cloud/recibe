(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear a)
    (handempty)
    (on b d)
    (on d a)
    (on f b)
    (on e f)
    (on c e)
    (ontable c)
  )
  (:goal (and
    (on e f)
    (on f a)
    (on a b)
    (on b c)
    (on c d)
  ))
)
