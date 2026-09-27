(define (problem blocks-stack)
  (:domain BLOCKS)
  (:objects
    a b c d e - block
  )
  (:init
    (on a b)
    (on c a)
    (on e c)
    (on d e)
    (ontable b)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b e)
    (on e a)
  ))
)
