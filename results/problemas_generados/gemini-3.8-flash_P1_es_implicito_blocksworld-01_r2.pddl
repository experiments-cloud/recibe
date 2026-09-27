(define (problem blocksworld-cinco-bloques)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (clear d)
    (handempty)
    (on a b)
    (on c a)
    (on d e)
    (on e c)
    (ontable b)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b e)
    (on e a)
  ))
)
