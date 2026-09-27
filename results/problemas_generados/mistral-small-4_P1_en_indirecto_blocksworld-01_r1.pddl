(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (clear d)
    (handempty)
    (on a b)
    (on b e)
    (on c a)
    (on e c)
    (ontable d)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b e)
    (on e a)
  ))
)
