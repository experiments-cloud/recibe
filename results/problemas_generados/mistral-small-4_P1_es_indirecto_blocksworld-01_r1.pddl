(define (problem blocksworld-problema)
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
    (on d c)
    (ontable e)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b e)
    (on e a)
  ))
)
