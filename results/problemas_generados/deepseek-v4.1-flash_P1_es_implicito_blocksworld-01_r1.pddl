(define (problem blocksworld-problema)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (clear d)
    (handempty)
    (on a b)
    (on c a)
    (on e c)
    (on d e)
    (ontable b)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b e)
    (on e a)
  ))
)
