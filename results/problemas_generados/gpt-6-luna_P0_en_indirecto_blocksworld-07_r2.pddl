(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f g - block
  )
  (:init
    (on a d)
    (ontable d)
    (clear a)
    (on b c)
    (on c g)
    (on g e)
    (on e f)
    (ontable f)
    (clear b)
    (handempty)
  )
  (:goal
    (and
      (on e b)
      (on b f)
      (on f d)
      (on d a)
      (on a c)
      (on c g)
    )
  )
)
