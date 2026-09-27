(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (clear d)
    (handempty)
    (ontable b)
    (on a b)
    (on c a)
    (on e c)
    (on d e)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b e)
    (on e a)
  ))
)
