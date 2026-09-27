(define (problem blocksworld-problema)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (clear d)
    (handempty)
    (on e d)
    (on c e)
    (on a c)
    (on b a)
    (ontable b)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b e)
    (on e a)
  ))
)
